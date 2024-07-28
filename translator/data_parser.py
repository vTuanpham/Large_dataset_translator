import math
import re
import json
import os
import random
import string
import sys
sys.path.insert(0, r'./')
from copy import deepcopy

import threading
import warnings
import traceback
try:
    from google.colab import files
    IN_COLAB = True
except ImportError:
    IN_COLAB = False
from httpcore._exceptions import ConnectTimeout
from typing import List, Dict, Union
from abc import abstractmethod
from tqdm.auto import tqdm

from concurrent.futures import ThreadPoolExecutor

from providers import Provider, GoogleProvider, MultipleProviders
from configs import BaseConfig, QAConfig, DialogsConfig, CorpusConfig
from .utils import force_super_call, ForceBaseCallMeta, timeit, have_internet
from .filters import have_code, have_re_code


if not have_internet(timeout=5):
    raise ConnectTimeout("Please provide internet connection as this script require external api calls")


class DataParser(metaclass=ForceBaseCallMeta):
    def __init__(self, file_path: str,
                 output_dir: str,
                 parser_name: str,
                 target_fields: List[str],
                 target_config: Union[BaseConfig, QAConfig, DialogsConfig, CorpusConfig],
                 do_translate: bool = False,
                 enable_sub_task_thread: bool = True,  # Enable splitting a large list into sublist if a list of one example is too large to process
                                                       # This argument go with max_list_length_per_thread
                 no_translated_code: bool = False,
                 max_example_per_thread: int = 400,  # How many examples, each thread can contain
                 large_chunks_threshold: int = 20000,  # Maximum number of examples that will be distributed evenly across threads, any examples exceed this threshold will be process in queue
                 max_list_length_per_thread: int = 3,  # Maximum number of strings contain in a list in a single thread.
                                                       # if larger, split the list into sub-list and process in parallel
                 translator: Provider = GoogleProvider,
                 source_lang: str = "en",
                 target_lang: str = "vi",
                 fail_translation_code: str="P1OP1_F"  # Fail code for *expected* fail translation and can be removed
                                                       # post-translation
                 ) -> None:

        self.data_read = None
        self.converted_data = None
        self.file_path = file_path
        self.output_dir = output_dir
        assert os.path.isdir(self.output_dir), "Please provide the correct output directory"

        self.parser_name = parser_name
        assert target_config, "Please specified the target config (Choose from the configs dir)"
        self.target_config = target_config

        self.do_translate = do_translate

        if self.do_translate:
            self.fail_translation_code = fail_translation_code
            self.enable_sub_task_thread = enable_sub_task_thread
            self.source_lang = source_lang
            self.target_lang = target_lang
            assert target_fields, f"Please specified target fields to be translate from the {self.target_config} config"
            self.target_fields = target_fields
            assert set(self.target_fields).issubset(set(self.target_config.get_keys())), \
                f"The target fields {self.target_fields} do not exist in the target config {self.target_config.get_keys()}"
            self.no_translated_code = no_translated_code
            assert max_example_per_thread < large_chunks_threshold, \
                " Large chunks threshold can't be smaller than max_example per thread!"
            self.max_example_per_thread = max_example_per_thread
            self.large_chunks_threshold = large_chunks_threshold
            if self.enable_sub_task_thread:
                self.max_list_length_per_thread = max_list_length_per_thread

            self.converted_data_translated = None

            self.translator = translator

    @property
    def get_translator(self) -> Provider:
        return deepcopy(self.translator)()

    @staticmethod
    def id_generator(size=6, chars=string.ascii_uppercase + string.digits) -> str:
        return ''.join(random.choice(chars) for _ in range(size))

    @staticmethod
    def split_list(input_list: List[str], max_sub_length: int) -> List[list]:
        return [input_list[x:x + max_sub_length] for x in range(0, len(input_list), max_sub_length)]

    def validate(self, keys: List[str]) -> bool:
        dict_fields = self.target_config.get_keys()
        for key in dict_fields:
            assert key in keys, f"\n Invalid parser, the key '{key}' is missing from {dict_fields}\n" \
                                f"you can adjust the fields {self.target_config.__name__} in the 'configs/*.py'" \
                                f"  or fill in the missing field"
        return True

    @timeit
    def pre_translate_validate(self) -> None:
        validated_translate_data = []
        # Note: This validates will override the original self.converted_data
        for idx, example in enumerate(tqdm(self.converted_data, desc="Validating data for translation:")):
            for key in self.target_fields:
                if self.no_translated_code:
                    example_filters = 0
                    contain_code, score, found_elements = have_code(example[key])
                    if contain_code:
                        example_filters += 1
                        if len(self.converted_data) - 2 == idx:
                            tqdm.write(f"Number of example with code: {example_filters}")
                        break
                    elif key == self.target_fields[-1]:
                        validated_translate_data.append(example)
                else:
                    if key == self.target_fields[-1]: validated_translate_data.append(example)

        print(f"\nTotal data left after filtering for translation: {len(validated_translate_data)}\n")
        self.converted_data = validated_translate_data

    @timeit
    def post_translate_validate(self) -> None:
        post_validated_translate_data = []
        # Note: This validates will override the original self.converted_data_translated
        for idx, example in enumerate(tqdm(self.converted_data_translated, desc="Validating data after translation:")):
            for key in self.target_fields:
                example_filters = 0
                if have_re_code(example[key], code=self.fail_translation_code):
                    example_filters += 1
                    if len(self.converted_data_translated) - 2 == idx:
                        tqdm.write(f"Number of example with fail code: {example_filters}")
                    break
                elif key == self.target_fields[-1]:
                    post_validated_translate_data.append(example)

        print(f"\nTotal data left after filtering fail translation: {len(post_validated_translate_data)}\n")
        self.converted_data_translated = post_validated_translate_data

    def __translate_per_key(self, example: Dict, translator: Provider = None, progress_idx: int = 0) -> Dict:
        '''
        This function loop through each key of one example and send to __translate_texts if the value of the key is
        under a certain threshold. If exceeded, then send to __sublist_multithread_translate
        '''

        assert self.do_translate, "Please enable translate via self.do_translate"
        keys = self.target_config.get_keys()
        for key in keys:
            if key in self.target_fields:
                type = "str" if isinstance(example[key], str) else "list"
                if example[key] == "":
                    continue
                if type == "list":
                    for data in example[key]:
                        if len(data) > 15000:
                            warnings.warn("Example" + example["qas_id"] + " have field len larger than 15000")
                            example[key].append(data[:15000])
                else:
                    if len(example[key]) > 15000:
                        warnings.warn("Example" + example["qas_id"] + " have field len larger than 15000")
                        example[key] = example[key][:15000]

                if self.enable_sub_task_thread:
                    average_length_sub_task_criteria = False
                    if type == "list" and len(example[key]) > 2:
                        average_length = sum(len(lst) for lst in example[key]) / len(example[key])
                        if average_length > 1600: average_length_sub_task_criteria = True
                    if type == "list" and average_length_sub_task_criteria and len(example[key]) >= self.max_list_length_per_thread:
                        # tqdm.write(f"\nSplitting {key} field which contain {len(example[key])} items on chunk {progress_idx}\n")
                        del translator
                        example[key] = self.__sublist_multithread_translate(example[key],
                                                                            progress_idx,
                                                                            key)
                    else:
                        example[key] = self.__translate_texts(src_texts=example[key], translator=translator)
                else:
                    example[key] = self.__translate_texts(src_texts=example[key], translator=translator)

        return example

    def __sublist_multithread_translate(self,
                                       list_str: List[str],
                                       progress_idx: int = 0,
                                       field_name: str=None # The field name (key name) of one example that exceed a certain threshold and needed to be split and translate in parallel
                                       ) -> List[str]:
        '''
        This function split a large list into sub-list and translate it in parallel, orders are maintained when merge all
        sub-lists, this is useful when order are necessary (e.g Dialogs example)
        '''

        translated_list_data = []
        num_threads = len(list_str) / self.max_list_length_per_thread
        sub_str_lists = self.split_list(list_str, max_sub_length=self.max_list_length_per_thread)
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = []
            finished_task = 0
            lock = threading.RLock()

            def callback_sub_list_done(future):
                nonlocal translated_list_data
                nonlocal finished_task
                nonlocal lock
                if not future.exception():
                    with lock:
                        # This need to be .append to keep the list structure
                        # Since this deal with sub-list and needed to be merged later
                        translated_list_data.append(future.result())
                        finished_task += 1
                else:
                    tqdm.write(f"Sub task of chunk {progress_idx} with field {field_name} failed with the following error: {future.exception()}."
                               f"Restarting thread when others finished...")
                pass

            for idx, list_chunk in enumerate(sub_str_lists):
                # Assign each thread with a new Translator instance
                future_chunk = executor.submit(self.__translate_texts,
                                               src_texts=list_chunk,
                                               translator=self.get_translator,
                                               sub_list_idx=idx)
                future_chunk.add_done_callback(callback_sub_list_done)
                future_dict = {
                    "future": future_chunk,
                    "idx": idx
                }
                futures.append(future_dict)

            # Wait for all threads to complete
            while finished_task < len(futures):
                for future_dict in futures:
                    # If exception occurs in one of the thread, restart the thread with its specific chunk
                    if future_dict['future'].exception():
                        tqdm.write(
                            f"Thread {future_dict['idx']} failed, restarting thread with chunk {future_dict['idx']}")
                        backup_future_chunk = executor.submit(self.__translate_texts,
                                                              src_texts=sub_str_lists[future_dict['idx']],
                                                              translator=self.get_translator,
                                                              sub_list_idx=future_dict['idx'])
                        backup_future_chunk.add_done_callback(callback_sub_list_done)
                        backup_future_dict = {"future": backup_future_chunk,
                                              "idx": future_dict['idx']}
                        futures[future_dict['idx']] = backup_future_dict
                        continue

            # Sorting the list of dictionaries based on the 'key' value
            translated_list_data = sorted(translated_list_data, key=lambda x: x['key'])
            # Extracting values after sorting
            translated_list_data = [item['text_list'] for item in translated_list_data]

            def flatten_list(nested_list):
                '''
                Turn a list from [[], [], []] -> []
                '''

                flattened_list = []
                for item in nested_list:
                    if isinstance(item, list):
                        flattened_list.extend(flatten_list(item))
                    else:
                        flattened_list.append(item)
                return flattened_list

            translated_list_data = flatten_list(translated_list_data)

            return translated_list_data

    def __translate_texts(self,
                          src_texts: Union[List[str], str],
                          translator: Provider = None,
                          sub_list_idx: int=None, # sub_list_idx is for pass through of index information and can be merge later by __sublist_multithread_translate
                          ) -> Union[List[str], str, Dict[List[str], int]]:
        '''
        Actual place where translation take place
        '''

        assert self.do_translate, "Please enable translate via self.do_translate"
        # This if is for multithread Translator instance
        translator_instance = deepcopy(self.translator)() if not translator else translator

        target_texts = translator_instance.translate(src_texts,
                                                     src=self.source_lang,
                                                     dest=self.target_lang,
                                                     fail_translation_code=self.fail_translation_code)

        return {'text_list': target_texts, 'key': sub_list_idx} if sub_list_idx is not None else target_texts

    def translate_converted(self,
                            en_data: List[str] = None,
                            desc: str = None,
                            translator: Provider = None,
                            large_chunk: List[str] = None) -> Union[None, List[str]]:
        '''
        This function support translation in multithread for large dataset
        (Does not maintain order for the final dataset)
        '''

        assert self.converted_data is not None or en_data is not None or large_chunk is not None, \
            "Please implement the convert function for DataParser " \
            "and assign converted_data to self.converted_data"

        if not en_data and not large_chunk:
            converted_data = self.converted_data
        elif not en_data:
            converted_data = large_chunk
        else:
            converted_data = en_data

        translated_data = []

        # Split large data into large chunks, recursive feed to the same function
        if len(converted_data) > self.large_chunks_threshold and large_chunk is None:
            num_large_chunks = len(converted_data) / self.large_chunks_threshold
            large_chunks = self.split_list(converted_data, max_sub_length=self.large_chunks_threshold)
            tqdm.write(
                f"Data is way too large, spliting data into {num_large_chunks} large chunk for sequential translation")

            for idx, large_chunk in enumerate(tqdm(large_chunks, desc=f"Translating large chunk ", colour="red")):
                tqdm.write(f"Processing large chunk No: {idx}")
                self.translate_converted(large_chunk=large_chunk)
            return None

        # Split large chunk into large example, recursive feed to the same function via multithread
        if len(converted_data) > self.max_example_per_thread and en_data is None:
            num_threads = len(converted_data) / self.max_example_per_thread
            chunks = self.split_list(converted_data, max_sub_length=self.max_example_per_thread)
            tqdm.write(f"Data too large, splitting data into {num_threads} chunk, each chunk is {len(chunks[0])}"
                       f" Processing with multithread...")

            # Progress bar
            desc = "Translating total converted large chunk data" if large_chunk else "Translating total converted data"
            progress_bar = tqdm(total=math.ceil(num_threads), desc=desc, position=math.ceil(num_threads)+1)

            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                futures = []
                finished_task = 0
                # https://stackoverflow.com/questions/22885775/what-is-the-difference-between-lock-and-rlock#22885810
                lock = threading.RLock()

                def callback_done(future):
                    nonlocal translated_data
                    nonlocal finished_task
                    nonlocal progress_bar
                    nonlocal lock
                    if not future.exception():
                        with lock:
                            # This need to be += or .extend to shallow flatten the list structure
                            translated_data += future.result()
                            finished_task += 1
                            progress_bar.update(1)
                    else:
                        tqdm.write(f"Task failed with the following error: {future.exception()}."
                                   f" Restarting thread when others finished")
                        pass

                for idx, chunk in enumerate(chunks):
                    # Assign each thread with a new Translator instance
                    future_chunk = executor.submit(self.translate_converted,
                                                   en_data=chunk,
                                                   desc=f"chunk {idx}",
                                                   translator=self.get_translator)
                    future_chunk.add_done_callback(callback_done)
                    future_dict = {"future": future_chunk,
                                   "idx": idx}
                    futures.append(future_dict)

                # Wait for all threads to complete
                while finished_task < len(futures):
                    for future_dict in futures:
                        # If exception occurs in one of the thread, restart the thread with its specific chunk
                        if future_dict['future'].exception():
                            tqdm.write(
                                f"Thread {future_dict['idx']} failed, restarting thread with chunk {future_dict['idx']}")
                            backup_future_chunk = executor.submit(self.translate_converted,
                                                                  en_data=chunks[future_dict['idx']],
                                                                  desc=f"Backup chunk {future_dict['idx']}",
                                                                  translator=self.get_translator)
                            backup_future_chunk.add_done_callback(callback_done)
                            backup_future_dict = {"future": backup_future_chunk,
                                                  "idx": future_dict['idx']}
                            futures[future_dict['idx']] = backup_future_dict
                            continue

            if large_chunk:
                if not self.converted_data_translated:
                    self.converted_data_translated = translated_data
                else:
                    self.converted_data_translated += translated_data
                return None

            self.converted_data_translated = translated_data
            return None

        progress_bar_desc = "Translating converted data" if not desc else f"Translating converted data {desc}"
        for example in tqdm(converted_data, desc=progress_bar_desc, colour="#add8e6"):
            translated_data_example = self.__translate_per_key(example,
                                                               translator,
                                                               progress_idx=int(re.findall(r'\d+', desc)[0]) if desc and re.findall(r'\d+', desc) else 0)
            translated_data.append(translated_data_example)
        if en_data: return translated_data
        if large_chunk:
            # Assuming that the previous large chunk process already create self.converted_data_translated
            # This cover the case where last large chunk only contain a single thread
            self.converted_data_translated += translated_data
        else:
            self.converted_data_translated = translated_data

    @abstractmethod
    @force_super_call
    def convert(self) -> Union[List[Dict], None]:
        assert self.data_read is not None, "Please implement the read function for DataParser" \
                                           " and assign data to self.data_read"
        pass

    @abstractmethod
    @force_super_call
    def read(self) -> Union[List, Dict, None]:
        assert os.path.isfile(self.file_path), f"Invalid path file for {self.file_path}"
        pass

    @property
    @force_super_call
    @timeit
    def save(self) -> None:
        '''
        Save the correct format that pyarrow supported, which is "line-delimited JSON" and can be load by
        huggingface-datasets load_datasets function
        '''
        output_path = os.path.join(self.output_dir, f"{self.parser_name}.json")
        with open(output_path, 'w', encoding='utf-8') as jfile:
            print(f"\n Saving {self.parser_name} to {output_path}... ")
            for idx, data in enumerate(tqdm(self.converted_data, desc="Writing data to file")):
                if self.validate(self.converted_data[idx].keys()):
                    jfile.write(json.dumps(data, ensure_ascii=False) + "\n")
            print(f"\n Total line printed: {idx + 1}")

        if IN_COLAB:
            print(f"\n Downloading converted data to local machine...")
            files.download(output_path)

        if self.do_translate:
            self.pre_translate_validate()
            self.translate_converted()
            self.post_translate_validate()
            assert self.converted_data_translated is not None, "Converted data haven't been translated yet!"
            output_translated_path = os.path.join(self.output_dir,
                                                  f"{self.parser_name}_translated_{self.target_lang}.json")
            with open(output_translated_path, 'w', encoding='utf-8') as jfile:
                print(f"\n Saving {self.parser_name} translated to {output_translated_path}... ")
                for idx, data in enumerate(
                        tqdm(self.converted_data_translated, desc="Writing translated data to file")):
                    jfile.write(json.dumps(data, ensure_ascii=False) + "\n")
                print(f"\n Total line printed: {idx + 1}")

            if IN_COLAB:
                print(f"\n Downloading converted translated data to local machine...")
                files.download(output_translated_path)
