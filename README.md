<p align="center">
  <img src="https://github.com/vTuanpham/Large_dataset_translator/assets/82665400/e424f17d-1c9e-4c72-90d2-9ef77c3b9dd2" width="100" height="100">
</p>


<div align="center">
  <h1>Large dataset translator</h1>
</div>

<p align="center">
  <a href="https://colab.research.google.com/drive/1OEni8c9N9C_9Kf3ySt87goN7HDvRN3nw?usp=sharing">
    <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab">
  </a>
</p>

![Test translation eli5 german](https://github.com/vTuanpham/Large_dataset_translator/actions/workflows/test_translate.yml/badge.svg?event=push)


### Here's the DataParser class in action, 1507 rows translated to Korean in under 2 minutes
![Translation demo](assets/Translate_demo.gif)

* ## Translating any large dataset to any language with the fraction of the time
    * Splitting large dataset into chunks and running translation in parallel via multithread processing
    * Any thread that fail will restart automatically with its specific chunk until all data point is fully translated
    * Convert into the same format that is support by pyarrow and huggingface-datasets
    * Filters can be use post translation
      * Remove examples that might contain code
        (Code example that have variable, function name,... will be translated by google)
    * Automatically download the converted dataset and the translated dataset if you're on colab upon finished
    * Unlimited translation, no api key required
* ### Dataset like ELI5, OpenOcra that have over 100k examples that will take up more than a 1000 hours on a single thread can be translate in under 2 hours 

* ## Setup
    #### Have python 3.8 or above
    ##### Setup on local machine
    ```sh
    git clone https://github.com/vTuanpham/Large_dataset_translator.git
     
    cd Large_dataset_translator
  
    # setup virtual env
    virtualenv trans-env
  
    # Activate virtual env
    source trans-env/bin/activate
  
    # Install package into virtual env
    pip install -r requirements.txt
    ```

    ##### Setup on colab
    ```sh
    !git clone https://github.com/vTuanpham/Large_dataset_translator.git
     
    %cd Large_dataset_translator
  
    %pip install -r requirements.txt
    ```
* ## Test
  #### This should take about 10-20mins on local or 5-10mins on colab
  ##### Running test on local machine
  ```sh
  python examples/YahmaAlpaca/AlpacaCleaned_Parser.py
  ```
  ##### Running test on colab [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1OEni8c9N9C_9Kf3ySt87goN7HDvRN3nw?usp=sharing)

  ```sh
  %run examples/YahmaAlpaca/AlpacaCleaned_Parser.py
  ```
  * Be sure to check the output in the examples/YahmaAlpaca dir, there should be an english version and a Vietnamese version
  * If all things go well, you should have your own dataset translated !
  * yahma/alpaca-cleaned datasets on huggingface-hub has 51.8k rows of data
  * Don't recommend ctrl^C in the middle of translation
* ## Remember to leave a star 🌞 if the test was successful :)
    ## Translate your own dataset
    * #### Look through all the examples in the examples/ dir first !
    * Inherit the DataParser class and implement your read and convert logic
    * The convert function must map all fields from the original dataset to all fields in the configs/base_config.py
    * Set do_translate=True in the super call like so:
      ```python
      def __init__(self, file_path: str, output_path: str):
        super().__init__(file_path, output_path,
                         parser_name=PARSER_NAME,
                         do_translate=True,
                         no_translated_code=True,
                         target_lang="ko")
      ```
    * Set no_translated_code=True to enable no string that might contain code to be translated
    * Set target_lang to the correct language that you want to be translated
    * Set source_lang if the source dataset is not in english
      
    * Be sure your converted data from the convert function must have the following fields for each row of data:
      ```python
      @dataclass
      class BaseConfig:
          """
          A single training/test example for base config.
          """
          qas_id: str
          system_prompt: str
      
          question_text: str
      
          orig_answer_texts: str = None
          answer_lengths: int = None
      ```
      ```sh
      {
       "system_prompt": "",
       "qas_id": "VA4KDG",
       "question_text": "Give three tips for staying healthy. ",
       "orig_answer_texts": "1. Eat a balanced and nutritious diet: Make sure your meals are inclusive of a variety of fruits and vegetables, lean protein, whole grains, and healthy fats. This helps to provide your body with the essential nutrients to function at its best and can help prevent chronic diseases.\n\n2. Engage in regular physical activity: Exercise is crucial for maintaining strong bones, muscles, and cardiovascular health. Aim for at least 150 minutes of moderate aerobic exercise or 75 minutes of vigorous exercise each week.\n\n3. Get enough sleep: Getting enough quality sleep is crucial for physical and mental well-being. It helps to regulate mood, improve cognitive function, and supports healthy growth and immune function. Aim for 7-9 hours of sleep each night.",
       "answer_lengths": null
      }
      ```
      Or you can create a new config @dataclass and change the self.target_config :D
      * Note: Each example must be a dict 
* ## Here is the list of all available languages:

  <table>
    <tr>
      <th>Languages</th>
      <th>Code</th>
    </tr>
    <tr>
      <td>Amharic</td>
      <td>am</td>
    </tr>
    <tr>
      <td>Arabic</td>
      <td>ar</td>
    </tr>
    <tr>
      <td>Basque</td>
      <td>eu</td>
    </tr>
    <tr>
      <td>Bengali</td>
      <td>bn</td>
    </tr>
    <tr>
      <td>English (UK)</td>
      <td>en-GB</td>
    </tr>
    <tr>
      <td>Portuguese</td>
      <td>pt-BR</td>
    </tr>
    <tr>
      <td>Bulgarian</td>
      <td>bg</td>
    </tr>
    <tr>
      <td>Catalan</td>
      <td>ca</td>
    </tr>
    <tr>
      <td>Cherokee</td>
      <td>chr</td>
    </tr>
    <tr>
      <td>Croatian</td>
      <td>hr</td>
    </tr>
    <tr>
      <td>Czech</td>
      <td>cs</td>
    </tr>
    <tr>
      <td>Danish</td>
      <td>da</td>
    </tr>
    <tr>
      <td>Dutch</td>
      <td>nl</td>
    </tr>
    <tr>
      <td>English</td>
      <td>en</td>
    </tr>
    <tr>
      <td>Estonian</td>
      <td>et</td>
    </tr>
    <tr>
      <td>Finnish</td>
      <td>fi</td>
    </tr>
    <tr>
      <td>French</td>
      <td>fr</td>
    </tr>
    <tr>
      <td>German</td>
      <td>de</td>
    </tr>
    <tr>
      <td>Greek</td>
      <td>el</td>
    </tr>
    <tr>
      <td>Gujarati</td>
      <td>gu</td>
    </tr>
    <tr>
      <td>Hebrew</td>
      <td>iw</td>
    </tr>
    <tr>
      <td>Hindi</td>
      <td>hi</td>
    </tr>
    <tr>
      <td>Hungarian</td>
      <td>hu</td>
    </tr>
    <tr>
      <td>Icelandic</td>
      <td>is</td>
    </tr>
    <tr>
      <td>Indonesian</td>
      <td>id</td>
    </tr>
    <tr>
      <td>Italian</td>
      <td>it</td>
    </tr>
    <tr>
      <td>Japanese</td>
      <td>ja</td>
    </tr>
    <tr>
      <td>Kannada</td>
      <td>kn</td>
    </tr>
    <tr>
      <td>Korean</td>
      <td>ko</td>
    </tr>
    <tr>
      <td>Latvian</td>
      <td>lv</td>
    </tr>
    <tr>
      <td>Lithuanian</td>
      <td>lt</td>
    </tr>
    <tr>
      <td>Malay</td>
      <td>ms</td>
    </tr>
    <tr>
      <td>Malayalam</td>
      <td>ml</td>
    </tr>
    <tr>
      <td>Marathi</td>
      <td>mr</td>
    </tr>
    <tr>
      <td>Norwegian</td>
      <td>no</td>
    </tr>
    <tr>
      <td>Polish</td>
      <td>pl</td>
    </tr>
    <tr>
      <td>Portuguese (PT)</td>
      <td>pt-PT</td>
    </tr>
    <tr>
      <td>Romanian</td>
      <td>ro</td>
    </tr>
    <tr>
      <td>Russian</td>
      <td>ru</td>
    </tr>
    <tr>
      <td>Serbian</td>
      <td>sr</td>
    </tr>
    <tr>
      <td>Chinese (CN)</td>
      <td>zh-CN</td>
    </tr>
    <tr>
      <td>Slovak</td>
      <td>sk</td>
    </tr>
    <tr>
      <td>Slovenian</td>
      <td>sl</td>
    </tr>
    <tr>
      <td>Spanish</td>
      <td>es</td>
    </tr>
    <tr>
      <td>Swahili</td>
      <td>sw</td>
    </tr>
    <tr>
      <td>Swedish</td>
      <td>sv</td>
    </tr>
    <tr>
      <td>Tamil</td>
      <td>ta</td>
    </tr>
    <tr>
      <td>Telugu</td>
      <td>te</td>
    </tr>
    <tr>
      <td>Thai</td>
      <td>th</td>
    </tr>
    <tr>
      <td>Chinese (TW)</td>
      <td>zh-TW</td>
    </tr>
    <tr>
      <td>Turkish</td>
      <td>tr</td>
    </tr>
    <tr>
      <td>Urdu</td>
      <td>ur</td>
    </tr>
    <tr>
      <td>Ukrainian</td>
      <td>uk</td>
    </tr>
    <tr>
      <td>Vietnamese</td>
      <td>vi</td>
    </tr>
    <tr>
              <td>Welsh</td>
              <td>cy</td>
            </tr>
          </table>

* Known issues: 
  * 'TypeError: "NoneType' object is not iterable"
     This issue is relevant to gender-specific translation, you can read more here https://github.com/ssut/py-googletrans/issues/260


