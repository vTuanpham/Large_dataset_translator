import random
import sys

sys.path.insert(0,r'./')
from tqdm.auto import tqdm

from datasets import load_dataset

from configs import BaseConfig
from translator import DataParser, VerboseCallback
from providers import GroqProvider


PARSER_NAME = "MagpieUltraV01"

# Patience is the key since the data is large and using LLM based translator
class MagpieUltraV01Parser(DataParser):
    def __init__(self, file_path: str, output_path: str):
        super().__init__(file_path, output_path,
                         parser_name=PARSER_NAME,
                         target_config=BaseConfig,   # The data config to be validated to check if self implement "convert" function is correct or not,
                                                     # you must map the data form to the correct fields of the @dataclass in the configs/base_config.py
                         target_fields=['question_text', 'orig_answer_texts'],   # The data fields to be translated (The fields belong to BaseConfig)
                         do_translate=True,
                         no_translated_code=False,
                         translator=GroqProvider,
                         parser_callbacks=[VerboseCallback],
                         max_example_per_thread=400,
                         large_chunks_threshold=2000)  # The callback to be called after the data has been converted and translated

    # Read function must assign data that has been read to self.data_read
    def read(self) -> None:
        # The read function must call the read function in DataParser class
        # I just want to be sure that the file path is correct
        super(MagpieUltraV01Parser, self).read()

        # OpenOcra is pretty large, so adjust accordingly
        self.data_read = load_dataset("argilla/magpie-ultra-v0.1")
        self.system_prompts = load_dataset("teilomillet/system_prompt")

        return None

    # Convert function must assign data that has been converted to self.converted_data
    def convert(self) -> None:
        # The convert function must call the convert function in DataParser class
        # I just want to be sure the read function has actually assigned the self.data_read
        super(MagpieUltraV01Parser, self).convert()

        data_converted = []
        for split in self.data_read:
            for data in tqdm(self.data_read[split], desc=f"Converting {split} data"):
                data_dict = {}
                random_index = random.randint(0, len(self.system_prompts['train']) - 1)
                data_dict['system_prompt'] = self.system_prompts['train'][random_index]['prompt']
                data_dict['qas_id'] = self.id_generator()
                data_dict['question_text'] = data['instruction']
                data_dict['orig_answer_texts'] = data['response']
                data_dict['answer_lengths'] = None

                data_converted.append(data_dict)

        # Be sure to assign the final data list to self.converted_data
        self.converted_data = data_converted[:2000]

        return None


if __name__ == '__main__':
    magpie_ultra_v01_parser = MagpieUltraV01Parser(r"examples/argilla-magpie-ultra-v0.1/dummy.txt",
                                                   r"examples/argilla-magpie-ultra-v0.1")
    magpie_ultra_v01_parser.read()
    magpie_ultra_v01_parser.convert()
    magpie_ultra_v01_parser.save
