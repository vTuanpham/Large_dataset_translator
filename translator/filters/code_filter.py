import re
from typing import Tuple, Union, List


def code_likelihood_score(text: str) -> Tuple[int, list]:
    # Calculate a score based on code-like elements
    score = 0
    code_elements = [
        ';', '{', '}', 'function', 'class', 'var', 'int', 'void', 'public',
        'import', 'for', 'while', 'elif', 'switch', 'case', 'break',
        'def', 'return', 'const', 'let', 'async', 'await', 'public', 'private',
        'protected', 'extends', 'implements', 'new', 'try', 'catch', 'throw',
        'require', 'import', 'module.exports', 'console.log', 'printf', '#include',
        'namespace', 'using', 'struct', 'typedef', 'enum', 'interface', 'const',
        'final', 'abstract', 'static', 'main', 'int', 'float', 'double', 'bool',
        'true', 'false', 'NULL', 'nil', 'void', 'var', 'let', 'const', 'val',
        'try', 'catch', 'finally', 'raise', 'lambda', 'self', 'super',
        'instanceof', 'enum', 'switch', 'case', 'break', 'default', 'console', 'python',
        'csharp' , 'c', 'js', 'javascript', 'java', 'pytorch', 'php', 'asm', '//', '#', 'writeline', 'readline', '```',
        'json', 'html', 'css', 'lxml', 'xml', '<', '>', '<html>', '<body>', '<li>', '</html>', '</body>', '</ul>', '<ul>', '</li>',
        '[', ']', '<text>', '</', '<source>', '</source>' , '</text>', 'sql', 'select', 'from' , 'table', 'union', 'group' ,
        'string', '()', 'Hello, world!', 'C# code', 'python code', 'import re', 'object', 'ABC', 'Ruby', 'regex', 'println'
    ]
    text = text.lower()  # Convert the text to lowercase for case-insensitive comparison
    found_elements = []
    for element in code_elements:
        element = element.lower()  # Convert elements to lowercase for case-insensitive comparison
        matches = re.finditer(rf'\b{re.escape(element)}\b', text)
        found_elements.extend([match.group() for match in matches])
    score += len(found_elements) # / (len(text.split(" ")) * 0.1)

    return score, found_elements


def have_code(text: Union[str, List[str]], threshold: int=8) -> Tuple[bool, int, list]:
    # threshold = len(text.split(" ")) * threshold
    if isinstance(text, list):
        threshold *= 2
        score = 0
        found_elements = []
        for str_text in text:
            sub_score, found_sub_elements = code_likelihood_score(str_text)
            score += sub_score
            found_elements += found_sub_elements
    else:
        score, found_elements = code_likelihood_score(text)

    if score >= threshold:
        return True, score, found_elements
    return False, score, found_elements


if __name__ == "__main__":
    code_text =[\
    '''
Can you generate a title that accurately reflects the impact of the pandemic on the hospitality industry? To help you out, use this Python code to extract keywords with five or more letters from this passage about the industry's response to new health and safety protocols:
```
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

    if have_code(code_text)[0]:
        print("IS CODE")
        print(have_code(code_text)[1])
    else:
        print("NO CODE")
        print(have_code(code_text)[1])

