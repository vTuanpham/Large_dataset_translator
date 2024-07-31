import json
import sys

sys.path.insert(0, r"./")
from tqdm.auto import tqdm
from datasets import load_dataset

from configs import KTOConfig
from translator import ParserCallback, VerboseCallback
from translator import DataParser


PARSER_NAME = "KTOmix14k"


class KTOPostProcessCallback(ParserCallback):
    def __init__(self) -> None:
        super().__init__()
        self.temp_parsed_unprocessed_data = [] # Store the unprocessed converted data

    def on_finish_convert(self, instance):
        process_converted_data = []
        self.temp_parsed_unprocessed_data = instance.converted_data
        print(f"Converted data length: {len(instance.converted_data)}")
        for data in instance.converted_data:
            process_converted_data.append(KTOConfig.construct_kto_example(
                data["conversation_history"],
                data["conversation_roles"],
                data["agent_prompt_completion"],
                data["label"],
                system_prompt=data["system_prompt"],
            ))
            process_converted_data[-1]["qas_id"] = data["qas_id"]
        instance.converted_data = process_converted_data
    
    def on_finish_save(self, instance):
        instance.converted_data = self.temp_parsed_unprocessed_data # Revert back to the unprocessed converted data as the processed data has been saved
        # The parser only work with string and list of strings, so we need to convert the data to string for the translator to work

    def on_finish_translate(self, instance):
        process_translated_data = []
        print(f"Translated data length: {len(instance.converted_data_translated)}")
        for translated_data in instance.converted_data_translated:
            process_translated_data.append(KTOConfig.construct_kto_example(
                translated_data["conversation_history"],
                translated_data["conversation_roles"],
                translated_data["agent_prompt_completion"],
                translated_data["label"],
                system_prompt=translated_data["system_prompt"],
            ))
            process_translated_data[-1]["qas_id"] = translated_data["qas_id"]
        instance.converted_data_translated = process_translated_data


class KTOmix14k(DataParser):
    def __init__(
        self,
        file_path: str,
        output_path: str,
        target_lang: str = "vi",
        max_example_per_thread=300,
        large_chunks_threshold=20000,
        max_list_length_per_thread=3,
    ):

        super().__init__(
            file_path,
            output_path,
            parser_name=PARSER_NAME,
            do_translate=True,
            no_translated_code=True,
            target_config=KTOConfig,
            target_fields=[
                "system_prompt",
                "conversation_history",
                "agent_prompt_completion",
            ],
            target_lang=target_lang,
            max_example_per_thread=max_example_per_thread,
            large_chunks_threshold=large_chunks_threshold,
            max_list_length_per_thread=max_list_length_per_thread,
            parser_callbacks=[KTOPostProcessCallback, VerboseCallback],
        )

    # Read function must assign data that has been read to self.data_read
    def read(self) -> None:
        # The read function must call the read function in DataParser class
        # I just want to be sure that the file path is correct
        super(KTOmix14k, self).read()

        # OpenOcra is pretty large, so adjust accordingly
        self.data_read = load_dataset("trl-lib/kto-mix-14k")

        return None

    def convert(self) -> None:
        # The convert function must call the convert function in DataParser class
        # I just want to be sure the read function has actually assigned the self.data_read
        super(KTOmix14k, self).convert()

        data_converted = []
        for split in self.data_read:
            for data in tqdm(self.data_read[split], desc=f"Converting data split {split}"):
                data_dict = {}
                system_prompt = None
                conversation_history = []
                conversation_roles = []

                for turn in data["prompt"]:
                    if turn["role"] == "system":
                        system_prompt = turn["content"]
                    else:
                        conversation_history.append(turn["content"])
                        conversation_roles.append(turn["role"])
                
                if system_prompt is None:
                    data_dict["system_prompt"] = None

                data_dict["qas_id"] = self.id_generator() 
                data_dict["conversation_history"] = conversation_history
                data_dict["conversation_roles"] = conversation_roles
                data_dict["agent_prompt_completion"] = data["completion"][0]["content"]
                data_dict["label"] = data["label"]
                data_converted.append(data_dict)

        # Be sure to assign the final data list to self.converted_data
        self.converted_data = data_converted

        return None


if __name__ == "__main__":
    kto_14k_parser = KTOmix14k(
        r"examples/kto-mix-14k/dummy.txt",
        r"examples/kto-mix-14k"
    )
    kto_14k_parser.read()
    kto_14k_parser.convert()
    kto_14k_parser.save
