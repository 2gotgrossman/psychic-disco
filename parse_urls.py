from bs4 import BeautifulSoup
import requests
import string


def make_request(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    request = requests.get(url, headers=headers)
    if request.status_code == 200:
        return request.content
    else:
        return None

def clean_request(html):
    """
    Removes 'script' and 'style' text and removes all tags
    html: Text of GET request
 }   return: string
    """
    soup = BeautifulSoup(html, "html.parser")

    try:
        title = soup.title.string.strip()
    except AttributeError: # Website doesn't have a title or has empty title
        title = ""

    for s in soup(['script', 'style']):
        s.decompose()
    return title, ' '.join(soup.stripped_strings)


def create_word_tokens(text):
    """
    Removes punctuation, digits, and converts to ASCII
    text: Unicode text of parsed html page
    return: List of word tokens (ByteStrings)
    """
    word_list = text.split()

    translator = str.maketrans('','',string.punctuation)
    filtered_punctuation = map(lambda word: word.translate(translator), word_list)
    mapped_lowercase     = map(lambda word: word.lower(), filtered_punctuation)
    map_ascii            = map(lambda word: word.encode('ascii', 'ignore'), mapped_lowercase)
    drop_empties         = filter(lambda word: word, map_ascii)
    drop_digits          = filter(lambda word: not word.isdigit(), drop_empties)
    
    to_list = list(drop_digits)
    return to_list

if __name__ == "__main__":
    url = b"http://carrot.is/coding/nginx_introduction"
    request = make_request(url)
    title, cleaned = clean_request(request)
    parsed = create_word_tokens(cleaned)
    print("Title:", title)
    print("Parsed:",parsed)
    
    import sys
    print(sys.getsizeof(str(parsed)))
