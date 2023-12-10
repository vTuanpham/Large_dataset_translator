import re
from typing import Union, List


def have_re_code(text: Union[str, List[str]], code: str="P1OP1_F") -> bool:
    is_found = False
    if isinstance(text, list):
        for str_text in text:
            if code in str_text: is_found = True
    else:
        if code in text: is_found = True

    return is_found


if __name__ == "__main__":
    code_text =[\
    '''
Can you generate a title that accurately reflects the impact of the pandemic on the hospitality industry? To help you out, use this Python code to extract keywords with five or more letters from this passage about the industry's response to new health and safety protocols:
```
P1OP1_Frtfhbrth
import re
text = "The hospitality industry has faced significant challenges due to the pandemic, including the need to implement new health and safety protocols. Many hotels and restaurants have had to adapt quickly to these changes in order to ensure the safety of their customers and staff. This has resulted in increased costs and decreased revenue for many businesses. However, some companies have been able to innovate and find new ways to serve their customers, such as offering contactless delivery and online ordering options."
keywords = re.findall(r'\b\w{5,}\b', text)
```
Once you have your list of keywords, combine them with this title prompt: "Can You Solve the Puzzle and Craft a Title for This Hospitality Industry Passage?" Be sure that your title accurately reflects the impact of the pandemic on the industry. Good luck, puzzle master!
    ''',
        '''
    Can you generate a title that accurately reflects the impact of the pandemic on the hospitality industry? To help you out, use this Python code to extract keywords with five or more letters from this passage about the industry's response to new health and safety protocols:
    ```
    import re
    text = "The hospitality industry has faced significant challenges due to the pandemic, including the need to implement new health and safety protocols. Many hotels and restaurants have had to adapt quickly to these changes in order to ensure the safety of their customers and staff. This has resulted in increased costs and decreased revenue for many businesses. However, some companies have been able to innovate and find new ways to serve their customers, such as offering contactless delivery and online ordering options."
    keywords = re.findall(r'\b\w{5,}\b', text)
    ```
    Once you have your list of keywords, combine them with this title prompt: "Can You Solve the Puzzle and Craft a Title for This Hospitality Industry Passage?" Be sure that your title accurately reflects the impact of the pandemic on the industry. Good luck, puzzle master!
        '''
    ]
    print(have_re_code(code_text))

