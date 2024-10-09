import re
from urllib.request import urlopen
from collections import Counter
import os
from typing import List, Tuple

def fetch_text(url: str) -> str:
    """
    Fetch the text content from the given URL or load from cache if available.
    
    Args:
        url (str): The URL of the text file to fetch.
    
    Returns:
        str: The text content of the file.
    """
    cache_filename: str = os.path.basename(url)
    cache_path: str = os.path.join("cache", cache_filename)

    if os.path.exists(cache_path):
        with open(cache_path, 'r', encoding='utf-8') as file:
            return file.read()
    else:
        os.makedirs("cache", exist_ok=True)
        with urlopen(url) as response:
            text: str = response.read().decode('utf-8')
        
        with open(cache_path, 'w', encoding='utf-8') as file:
            file.write(text)
        
        return text

def process_text(text: str) -> List[str]:
    """
    Process the text by converting to lowercase. 
    Add all words in the text to a list and returns it.
    
    Args:
        text (str): The input text to process.
    
    Returns:
        List[str]: A list of words from the text.
    """
    words: List[str] = re.findall(r'\b\w+\b', text.lower())
    return words

def get_top_words(words: List[str], start: int, end: int) -> List[Tuple[str, int]]:
    """
    Get the top words by frequency within the specified range.
    
    Args:
        words (List[str]): The list of words to analyze.
        start (int): The starting rank (inclusive).
        end (int): The ending rank (inclusive).
    
    Returns:
        List[Tuple[str, int]]: A list of tuples containing (word, frequency) pairs.
    """
    word_counts: Counter = Counter(words)
    return word_counts.most_common()[start-1:end]

def main() -> None:
    """
    Main function to orchestrate the word frequency analysis.
    """
    url: str = "https://www.gutenberg.org/cache/epub/16317/pg16317.txt"
    
    text: str = fetch_text(url)
    words: List[str] = process_text(text)
    top_words: List[Tuple[str, int]] = get_top_words(words, 10, 20)
    
    print("Words ranked from 10th to 20th by frequency:")
    for word, count in top_words:
        print(f"{word}: {count}")

if __name__ == "__main__":
    main()