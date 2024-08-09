import os
import sys
import json

from typing import Union, List, Optional
import concurrent.futures

from pydantic import Field
sys.path.insert(0,r'./')
from groq import Groq

try:
    from .base_provider import Provider
    from .utils import *
except ImportError:
    from base_provider import Provider
    from utils import *


try:
    os.environ["GROQ_API_KEY"]
except KeyError:
    raise KeyError("Please set the environment variable GROQ_API_KEY")

# Max list length of 5, cache all prompt and remove old prompt if the length is greater than 5, fuzzy match the current prompt with the cache prompt and return the fail_translation_code if the similarity is greater than 0.8
CACHE_PROMPT = []


class GroqProvider(Provider):
    def __init__(self):
        self.groq_client = Groq(
            api_key=os.environ.get("GROQ_API_KEY"),
        )
        self.translator = self.groq_client.chat.completions.create

    def construct_schema_prompt(self, schema: dict) -> str:
        schema_prompt = "Please provide the JSON object with the following schema:\n"

        json_prompt = json.dumps({key: value["description"] for key, value in schema.items()}, indent=2)
        
        return schema_prompt + json_prompt

    @throttle(calls_per_minute=30, verbose=False)
    def _do_translate(self, input_data: Union[str, List[str]],
                      src: str, dest: str,
                      fail_translation_code:str = "P1OP1_F", # Pass in this code to replace the input_data if the exception is *unavoidable*, any example that contain this will be remove post translation
                      **kwargs) -> Union[str, List[str]]:

        data_type = "list" if isinstance(input_data, list) else "str"

        from_language_name = get_language_name(src)
        dest_language_name = get_language_name(dest)

        if data_type == "list":
            translation_fields = {}
            prompt = ""
            for i in range(len(input_data)):
                translation_fields[f"translation_{i}"] = (str, Field(..., description=f"The translated text for text_{i}"))
                prompt += f"-"*10+f"\n text_{i}: {input_data[i]}\n" + "-"*10

            Translation = create_dynamic_model("Translation", translation_fields)

            system_prompt = f"You are a helpful assistant that translates text from {from_language_name} to {dest_language_name}. You must consider things that should not be translated like names, places, code variables, etc. You should also consider the context of the text to provide the most accurate translation. You will only reply with the translation text and nothing else in JSON. \n\n{self.construct_schema_prompt(Translation.model_json_schema()['properties'])}"

            prompt += f"\n\nTranslate all the text above from {from_language_name} to {dest_language_name} and return the translations the corresonding fields in the JSON object."


        else:
            system_prompt = f"You are a helpful assistant that translates text from {from_language_name} to {dest_language_name}. You must consider things that should not be translated like names, places, code variables, etc. You should also consider the context of the text to provide the most accurate translation. Only reply with the translation text and nothing else."

            prompt = f"{input_data}\n\n Translate the above text from {from_language_name} to {dest_language_name}."
        
        chat_args = {
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "model": "gemma2-9b-it",
            "temperature": 0.7,
            "top_p": 0.5,
            "max_tokens": 8000,
            "frequency_penalty": 0.25,
            "presence_penalty": 0.25,
            "stream": False,
        }

        if data_type == "list":
            chat_args["response_format"] = {"type": "json_object"}
            
        if len((system_prompt+prompt).split()) > 8000:
            if data_type == "list": return [fail_translation_code, fail_translation_code]
            return fail_translation_code
        
        if len(CACHE_PROMPT) > 5:
            CACHE_PROMPT.pop(0)
        
        try:
            output = self.translator(**chat_args)
        except Exception as e:
            # Check if the exception is unavoidable by fuzzy matching the prompt with the cache prompt
            if fuzzy_match(input_data, CACHE_PROMPT, threshold=80):
                print(f"Unavoidable exception: {e}")
                if data_type == "list": return [fail_translation_code, fail_translation_code]
                return fail_translation_code
            else:
                CACHE_PROMPT.append(input_data)
            raise e

        if data_type == "list":
            output_text = output.choices[0].message.content
            output_schema = Translation.model_validate_json(output_text)
            output_dict = output_schema.model_dump()
            return [output_dict[f"translation_{i}"] for i in range(len(input_data))]
        else:
            return output.choices[0].message.content

def run_test_translation(test):
    print(test.translate(["Hello", "How are you today ?"], src="en", dest="vi"))
    print(test.translate("Hello", src="en", dest="vi"))

if __name__ == '__main__':
    test = GroqProvider()
    print(test.translate(["Hello", "How are you today ?"], src="en", dest="vi"))
    print(test.translate("Hello", src="en", dest="vi"))
    input_data = ["Hello", "How are you today ?"]
    src = "en"
    dest = "vi"

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(run_test_translation, GroqProvider()) for _ in range(30)]
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
            except Exception as e:
                print(f"Translation failed: {e}")

