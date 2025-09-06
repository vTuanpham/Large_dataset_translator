import json
import os
import sys
sys.path.insert(0, r'./')
from tqdm.auto import tqdm
from dataclasses import dataclass, field
import time

from configs import Config
from translator import DataParser, VerboseCallback

PARSER_NAME = "PerkeyKeyphrases"

@dataclass
class PerkeyConfig(Config):
    qas_id: str = None
    title: str = None
    summary: str = None
    body: str = None
    keyphrases: list = field(default_factory=list)
    category: str = None
    url: str = None
    
    @classmethod
    def get_keys(cls):
        return ['qas_id', 'title', 'summary', 'body', 'keyphrases', 'category', 'url']


class PerkeyKeyphrasesParser(DataParser):
    def __init__(self, file_path: str, output_path: str, target_lang: str="en",
                 max_example_per_thread=1000, large_chunks_threshold=100000):
        super().__init__(file_path, output_path,
                         parser_name=PARSER_NAME,
                         target_config=PerkeyConfig,  
                         target_fields=['title', 'summary', 'body', 'keyphrases', 'category'],  
                         do_translate=True,
                         no_translated_code=False,  
                         verbose=False,  
                         source_lang="fa",
                         target_lang=target_lang,
                         max_example_per_thread=max_example_per_thread,
                         large_chunks_threshold=large_chunks_threshold,
                         parser_callbacks=[VerboseCallback])

    def read(self) -> None:
        super(PerkeyKeyphrasesParser, self).read()

        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.data_read = json.load(f)
        
        print(f"Read {len(self.data_read)} records from {self.file_path}")
        return None

    def convert(self) -> None:
        super(PerkeyKeyphrasesParser, self).convert()

        data_converted = []
        for data in tqdm(self.data_read, desc="Converting data"):
            data_dict = {}
            
            data_dict['qas_id'] = self.id_generator()
            
            data_dict['title'] = data.get('title', '')
            data_dict['summary'] = data.get('summary', '')
            data_dict['body'] = data.get('body', '')
            data_dict['keyphrases'] = data.get('keyphrases', [])
            data_dict['category'] = data.get('category', '')
            
            data_dict['url'] = data.get('url', '')
            
            data_converted.append(data_dict)

        self.converted_data = data_converted
        print(f"Converted {len(self.converted_data)} records")

        return None

    def post_process(self):
        """Convert the translated data back to the original dataset structure"""
        if not hasattr(self, 'converted_data_translated') or not self.converted_data_translated:
            print("No translated data available to save in original format")
            return
            
        original_format = []
        for item in self.converted_data_translated:
            entry = {
                "title": item.get('title', ''),
                "category": item.get('category', ''),
                "keyphrases": item.get('keyphrases', []),
                "body": item.get('body', ''),
                "summary": item.get('summary', ''),
                "url": item.get('url', '')
            }
            original_format.append(entry)
        
        time_now = time.strftime("%Y%m%d-%H%M%S")

        output_path = os.path.join(self.output_dir, f'{self.parser_name}_translated_original_format_{time_now}.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(original_format, f, ensure_ascii=False, indent=4)
        
        print(f"Original format translated data saved to {output_path}")
        
        if original_format:
            print("\nSample of translated data in original format:")
            print(json.dumps(original_format[0], ensure_ascii=False, indent=2))


def process_file(input_path: str, output_dir: str, target_lang: str):
    os.makedirs(output_dir, exist_ok=True)
    
    parser = PerkeyKeyphrasesParser(
        file_path=input_path,
        output_path=output_dir,
        target_lang=target_lang
    )
    parser.read()
    parser.convert()
    
    try:
        parser.save
        parser.post_process()
    except Exception as e:
        print(f"Error during saving or post-processing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    # Process file - translating from Persian (fa) to English (en) - github.com/edoost/perkey/
    # process_file("./data/data.dev.json", "./data", target_lang="en")
    process_file("./data/data.test.json", "./data", target_lang="en")
    process_file("./data/data.train.json", "./data", target_lang="en")
    # process_file("./data/datasmall.dev.json", "./data", target_lang="en")

    
    print("\nTranslation completed. Check the output files in the ./data directory.")