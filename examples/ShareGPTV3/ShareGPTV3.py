import json
import random
import sys
sys.path.insert(0,r'./')
from tqdm.auto import tqdm

from configs import DialogsConfig
from translator import DataParser


PARSER_NAME = "ShareGPT_V3"


class ShareGPTV3(DataParser):
    def __init__(self, file_path: str, output_path: str, target_lang: str="vi",
                 max_example_per_thread=300, large_chunks_threshold=20000,
                 max_list_length_per_thread=3):
        super().__init__(file_path, output_path,
                         parser_name=PARSER_NAME,
                         do_translate=True,
                         no_translated_code=True,
                         target_config=DialogsConfig,
                         target_fields=['user_prompts', 'agent_responses'],
                         target_lang=target_lang,
                         max_example_per_thread=max_example_per_thread,
                         large_chunks_threshold=large_chunks_threshold,
                         max_list_length_per_thread=max_list_length_per_thread)

        # # The data config to be validated to check if self implement "convert" function is correct or not,
        # # you must map the data form to the correct fields of the @dataclass in the configs/base_config.py
        # self.target_config = DialogsConfig
        #
        # # The data fields to be translated (The fields belong to BaseConfig)
        # self.target_fields = ['user_prompts', 'agent_responses', 'hello']

    # Read function must assign data that has been read to self.data_read
    def read(self) -> None:
        # The read function must call the read function in DataParser class
        # I just want to be sure that the file path is correct
        super(ShareGPTV3, self).read()

        with open(self.file_path, encoding='utf-8') as jfile:
            json_data = json.load(jfile)

        self.data_read = json_data
        return None

    def convert(self) -> None:
        # The convert function must call the convert function in DataParser class
        # I just want to be sure the read function has actually assigned the self.data_read
        super(ShareGPTV3, self).convert()

        data_converted = []
        for data in tqdm(self.data_read, desc="Converting data"):
            data_dict = {}
            data_dict['system_prompt'] = ""
            data_dict['qas_id'] = data['id']

            user_prompts = []
            agent_responses = []
            for conversation in data['conversations']:
                if conversation["from"] == "human":
                    user_prompts.append(conversation['value'])
                if conversation["from"] == "gpt":
                    agent_responses.append(conversation['value'])

            data_dict['user_prompts'] = user_prompts
            data_dict['agent_responses'] = agent_responses

            data_dict['prompt_lengths'] = None
            data_dict['answer_lengths'] = None
            data_converted.append(data_dict)

        # Be sure to assign the final data list to self.converted_data
        self.converted_data = data_converted

        return None


if __name__ == '__main__':
    share_gpt_v3_parser = ShareGPTV3(r"examples/ShareGPTV3/ShareGPT_V3_unfiltered_cleaned_split.json",
                                     r"examples/ShareGPTV3")
    share_gpt_v3_parser.read()
    share_gpt_v3_parser.convert()
    share_gpt_v3_parser.save