# Large dataset translator
 * ## Translating any large dataset to any language with the fraction of the time
   * Spliting large dataset into chunks and running translation in parallel via multithread processing
   * Any thread that fail will restart automatically with its specific chunk until all data point is fully translated
   * Convert into the same format that is support by pyarrow and huggingface-datasets
   * Filters can be use post translation like remove example that might contain code
     (Code example that have variable, function name,... will be translated by google)
   * Automatically download the converted dataset and the translated dataset if you're on colab upon finished
   * Unlimited translation, no api key required
 * ### Dataset like ELI5, OpenOcra that have over 100k examples that will take up more than a 1000 hours on a single thread can be translate in under 2 hours 

 * ## Setup
     #### Have python 3.8 or above
     ```sh
     git clone https://github.com/vTuanpham/Large_dataset_translator.git
     
     cd Large_dataset_translator
  
     # setup virtual env
     virtualenv trans-env
  
     # Activate virtual env
     source trans-env/bin/activate
  
     # Install package into env
     pip install -r requirements.txt
     ```
  * ## Test
    #### This should take about 10-20mins on local or 5-10mins on colab
    ```sh
    python examples/YahmaAlpaca/AlpacaCleaned_Parser.py
    ```
    * Be sure to check the output in the examples/YahmaAlpaca dir, there should be an english version and a korea version
    * If all things go well, you should have your own dataset translated !
    * yahma/alpaca-cleaned datasets on huggingface-hub is 51.8k rows of data
    * Don't recommend ctrl+C in the middle of translation
* ## Remember to leave a star 🌞 if the test was successful :)
    ## Translate your own dataset
    * Look through all the examples in the examples/ dir first !
    * Inherit the DataParser class and implement your read and convert logic
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
      * Here the list of available languages:
        
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
              <td>Filipino</td>
              <td>fil</td>
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

