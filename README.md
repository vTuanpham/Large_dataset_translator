<p align="center">
  <img src="https://github.com/vTuanpham/Large_dataset_translator/assets/82665400/e424f17d-1c9e-4c72-90d2-9ef77c3b9dd2" width="100" height="100">
</p>

<div align="center">
  <h1>Large Dataset Translator</h1>
</div>

<p align="center">
  <a href="https://colab.research.google.com/drive/1OEni8c9N9C_9Kf3ySt87goN7HDvRN3nw?usp=sharing">
    <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab">
  </a>
</p>

![Test translation eli5 german](https://github.com/vTuanpham/Large_dataset_translator/actions/workflows/test_translate.yml/badge.svg?event=push)

The Large Dataset Translator is a robust solution crafted to effectively translate sizable datasets into diverse languages. It provides a smooth and parallelized translation process, guaranteeing swift outcomes without the need for an API key. The tool facilitates multithreaded processing, allowing users to translate extensive datasets in significantly less time. Additionally, it features an automatic fail-restart mechanism, ensuring the seamless continuation of the translation process in case of any interruptions. 

### Features

- **Parallelized Translation**: Utilizes multithread processing to split large datasets into chunks and translate in parallel, significantly reducing processing time.
  
- **Handling Large Lists**: Efficiently handles datasets containing large lists (e.g., dialogs) by splitting them into sub-lists and translating each sub-list in parallel.

- **Automatic Retry Mechanism**: Any thread that fails during translation will automatically restart with its specific chunk until all data points are fully translated.

- **Data Format Compatibility**: Converts datasets into a format supported by pyarrow and huggingface-datasets for seamless integration.

- **Pre-Translation Filters**: Filters can be applied before translation, such as removing examples that might contain code.

- **GIL Resilience**: Python Global Interpreter Lock (GIL) won't affect speed, as tasks consist of purely I/O-bound operations.

- **Automatic Download**: Automatically downloads the converted dataset and the translated dataset on Colab upon completion.

- **Unlimited Translation**: No API key is required, making it ideal for translating large datasets without limitations.

### Demonstration

Here's a demo of the DataParser class, translating 1507 rows of text to Korean in under 2 minutes:

![Translation demo](assets/Translate_demo.gif)

### Setup

#### Local Machine
```sh
git clone https://github.com/vTuanpham/Large_dataset_translator.git
     
cd Large_dataset_translator
  
# Set up virtual environment
virtualenv trans-env
  
# Activate virtual environment
source trans-env/bin/activate
  
# Install required packages
pip install -r requirements.txt
```
##### Google Colab
```sh
!git clone https://github.com/vTuanpham/Large_dataset_translator.git
 
%cd Large_dataset_translator

%pip install -r requirements.txt
```
### Testing
Run the provided test script to ensure the tool works correctly. This should take about 10-20 minutes on a local machine or 5-10 minutes on Colab.
##### Local Machine:
```sh
python examples/YahmaAlpaca/AlpacaCleaned_Parser.py
```
##### Colab [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1OEni8c9N9C_9Kf3ySt87goN7HDvRN3nw?usp=sharing)
```sh
%run examples/YahmaAlpaca/AlpacaCleaned_Parser.py
```
Check the examples/YahmaAlpaca directory when the script finished, there should be a parsed dataset and a vietnamese dataset. 

## Usage
### To translate your own dataset:
1.  Inherit the DataParser class and implement your read and convert logic.
2.  Ensure the convert function maps all fields from the original dataset to those in configs/base_config.py, or choose other configs that fit your dataset.
3.  Set do_translate=True in the super call to enable translation.
   
    ```python
      def __init__(self, file_path: str, output_path: str):
        super().__init__(file_path, output_path,
                         parser_name=PARSER_NAME,
                         do_translate=True,
                         no_translated_code=True,
                         target_lang="ko")
    ```
5.  Customize translation settings such as target language and pre-translation filters.
### Pull requests are welcome for new dataset conversion examples 😎
## Supported Languages
The tool supports translation into a wide array of languages. Refer to the table in google's documentation for the complete list.
https://cloud.google.com/translate/docs/languages
## Known Issues
  * 'TypeError: "NoneType' object is not iterable"
     This issue is relevant to gender-specific translation, you can read more here https://github.com/ssut/py-googletrans/issues/260
#### Feel free to star 🌟 the repository if the test was successful!
#### Disclaimer: This repo is for private use only.




