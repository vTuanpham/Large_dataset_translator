import sys
sys.path.insert(0,r'./')
from tqdm.auto import tqdm

from datasets import load_dataset

from configs import BaseConfig
from translator import DataParser


PARSER_NAME = "OpenOrca"


class OpenOrcaParser(DataParser):
    def __init__(self, file_path: str, output_path: str):
        super().__init__(file_path, output_path,
                         parser_name=PARSER_NAME,
                         do_translate=True,
                         no_translated_code=True)
        # The data config to be validated to check if self implement "convert" function is correct or not
        self.target_config = BaseConfig

        # The data fields to be translated (The fields belong to BaseConfig)
        self.target_fields = ['question_text', 'orig_answer_texts']

    # Read function must assign data that has been read to self.data_read
    def read(self) -> None:
        super(OpenOrcaParser, self).read()
        self.data_read = load_dataset("Open-Orca/OpenOrca")

        return None

    # Convert function must assign data that has been converted to self.converted_data
    def convert(self) -> None:
        super(OpenOrcaParser, self).convert()

        data_converted = []
        for split in self.data_read:
            for data in tqdm(self.data_read[split], desc=f"Converting {split} data"):
                data_dict = {}
                data_dict['system_prompt'] = data['system_prompt']
                data_dict['qas_id'] = data['id']
                data_dict['question_text'] = data['question']

                data_dict['orig_answer_texts'] = data['response']
                data_dict['answer_lengths'] = None
                data_converted.append(data_dict)

        self.converted_data = data_converted

        return None


if __name__ == '__main__':
    open_orca_parser = OpenOrcaParser(r"examples/OpenOrca/dummy.txt",
                                      r"examples/OpenOrca")
    open_orca_parser.read()
    open_orca_parser.convert()
    open_orca_parser.save
