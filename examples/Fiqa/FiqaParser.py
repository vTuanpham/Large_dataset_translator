import sys
import random
sys.path.insert(0,r'./')
from tqdm.auto import tqdm

from datasets import load_dataset

from configs import CorpusConfig
from translator import DataParser


PARSER_NAME = "FiqaParser"


class FiqaParser(DataParser):
    def __init__(self, file_path: str, output_path: str):
        super().__init__(file_path, output_path,
                         parser_name=PARSER_NAME,
                         target_config=CorpusConfig,    # The data config to be validated to check if self implement "convert" function is correct or not,
                                                        # you must map the data form to the correct fields of the @dataclass in the configs/base_config.py
                         target_fields=["orig_corpus_texts"],   # The data fields to be translated (The fields belong to BaseConfig)

                         do_translate=True,
                         no_translated_code=False,
                         target_lang="tr",
                         source_lang="en",)

    # Read function must assign data that has been read to self.data_read
    def read(self) -> None:
        # The read function must call the read function in DataParser class
        # I just want to be sure that the file path is correct
        super(FiqaParser, self).read()

        self.data_read = load_dataset("BeIR/fiqa" ,'corpus' , split='corpus')
        return None

    # Convert function must assign data that has been converted to self.converted_data
    def convert(self) -> None:
        # The convert function must call the convert function in DataParser class
        # I just want to be sure the read function has actually assigned the self.data_read
        super(FiqaParser, self).convert()

        system_prompts = [
            "Ensure clarity and fidelity to the original content.",
            "Maintain the integrity of the original content.",
            "You are here to help, preserve all critical details and nuances.",
            "Deliver a detailed and well-structured translation of the following content.",
            "Your purpose is to inform, provide a comprehensive translation.",
            "Ensure the original meaning and style are preserved.",
            "You are a virtual assistant, deliver a comprehensive translation.",
            "Provide an accurate and contextually appropriate translation of the following text.",
            "",
            "",
            "",
            "",
            "",
            "",
        ]

        data_converted = []
        for data in tqdm(self.data_read, desc=f"Converting data"):
            data_dict = {}
            # Randomly assign generic system prompt to data
            data_dict['system_prompt'] = random.choice(system_prompts)

            # The DataParser class has an id_generator method which can create random id for you
            data_dict['qas_id'] = data['_id']

            data_dict['orig_corpus_texts'] = data['text']
            data_dict['corpus_lengths'] = None
            data_converted.append(data_dict)

        # Be sure to assign the final data list to self.converted_data
        self.converted_data = data_converted

        return None


if __name__ == '__main__':
    alpaca_cleaned_parser = FiqaParser(r"examples/Fiqa/dummy.txt",
                                          r"examples/Fiqa")
    alpaca_cleaned_parser.read()
    alpaca_cleaned_parser.convert()
    alpaca_cleaned_parser.save
