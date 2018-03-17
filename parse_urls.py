from bs4 import BeautifulSoup
import requests
import string

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
page = requests.get('https://blog.ycombinator.com/13-companies-from-yc-winter-2018/', headers=headers)

def clean_request(html):
    """
    Removes 'script' and 'style' text and removes all tags
    html: Text of GET request
 }   return: string
    """
    soup = BeautifulSoup(html, "html.parser")
    for s in soup(['script', 'style']):
        s.decompose()
    return ' '.join(soup.stripped_strings)


def create_word_tokens(text):
    """
    Removes punctuation and converts to ASCII
    text: Unicode text of parsed html page
    return: List of word tokens (ByteStrings)
    """
    word_list = text.split(" ")

    translator = str.maketrans('','',string.punctuation)
    filtered_punctuation = map(lambda word: word.translate(translator), word_list)
    mapped_lowercase     = map(lambda word: word.lower(), filtered_punctuation)
    map_ascii            = map(lambda word: word.encode('ascii', 'ignore'), mapped_lowercase)
    drop_empties         = filter(lambda word: word, map_ascii)
    
    l = list(drop_empties)
    return l

cleaned = clean_request(page.content)
parsed = create_word_tokens(cleaned)
print(parsed)
