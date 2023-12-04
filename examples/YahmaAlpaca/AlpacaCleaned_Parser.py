import sys
import random
sys.path.insert(0,r'./')
from tqdm.auto import tqdm

from datasets import load_dataset

from configs import BaseConfig
from translator import DataParser


PARSER_NAME = "AlpacaCleaned"


class AlpacaCleaned(DataParser):
    def __init__(self, file_path: str, output_path: str):
        super().__init__(file_path, output_path,
                         parser_name=PARSER_NAME,
                         do_translate=True,
                         no_translated_code=True,
                         target_lang="vi")

        # The data config to be validated to check if self implement "convert" function is correct or not,
        # you must map the data form to the correct fields of the @dataclass in the configs/base_config.py
        self.target_config = BaseConfig

        # The data fields to be translated (The fields belong to BaseConfig)
        self.target_fields = ['question_text', 'orig_answer_texts']

    # Read function must assign data that has been read to self.data_read
    def read(self) -> None:
        # The read function must call the read function in DataParser class
        # I just want to be sure that the file path is correct
        super(AlpacaCleaned, self).read()

        self.data_read = load_dataset("yahma/alpaca-cleaned")

        return None

    # Convert function must assign data that has been converted to self.converted_data
    def convert(self) -> None:
        # The convert function must call the convert function in DataParser class
        # I just want to be sure the read function has actually assigned the self.data_read
        super(AlpacaCleaned, self).convert()

        system_prompts = [
            "You are an AI assistant, provide a detailed response.",
            "Imagine you are a knowledgeable expert, share your insights.",
            "You have vast knowledge, explain this clearly and comprehensively.",
            "As an AI language model, give a thorough and informative answer.",
            "You are here to help, please provide a detailed response.",
            "You possess a wealth of information, offer a complete explanation.",
            "Your purpose is to inform, provide a comprehensive response.",
            "You are designed to assist, offer a detailed and well-structured answer.",
            "You are a virtual assistant, deliver a comprehensive response.",
            "In your role as an AI, provide a detailed explanation.",
            "",
            "",
            ""
        ]

        data_converted = []
        for split in self.data_read:
            for data in tqdm(self.data_read[split], desc=f"Converting {split} data"):
                data_dict = {}
                # Randomly assign generic system prompt to data
                data_dict['system_prompt'] = random.choice(system_prompts)

                # The DataParser class has an id_generator method which can create random id for you
                data_dict['qas_id'] = self.id_generator()

                data_dict['question_text'] = data['instruction'] + " " + data['input']

                data_dict['orig_answer_texts'] = data['output']
                data_dict['answer_lengths'] = None
                data_converted.append(data_dict)

        # Be sure to assign the final data list to self.converted_data
        self.converted_data = data_converted

        return None


if __name__ == '__main__':
    alpaca_cleaned_parser = AlpacaCleaned(r"examples/YahmaAlpaca/dummy.txt",
                                          r"examples/YahmaAlpaca")
    alpaca_cleaned_parser.read()
    alpaca_cleaned_parser.convert()
    alpaca_cleaned_parser.save
