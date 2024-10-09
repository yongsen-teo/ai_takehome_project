import requests
import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Constants
API_URL = "https://api-inference.huggingface.co/models/openai-community/gpt2"
MAX_NEW_TOKENS = 50
NUM_RETURN_SEQUENCES = 1
TEMPERATURE = 0.8

def get_api_key() -> str:
    """
    Retrieve the API key from environment variables.
    
    Returns:
        str: The API key.
    
    Raises:
        ValueError: If the API key is not set in the environment.
    """
    api_key = os.getenv("HUGGINGFACE_API_KEY")
    if not api_key:
        raise ValueError("HUGGINGFACE_API_KEY is not set in the .env file.")
    return api_key

def create_headers(api_key: str) -> Dict[str, str]:
    """
    Create the headers for the API request.
    
    Args:
        api_key (str): The API key for authentication.
    
    Returns:
        Dict[str, str]: The headers for the API request.
    """
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "x-use-cache": "false"    # set to "true" to enable caching, "false" for real-time generation
    }

def create_payload(input_text: str) -> Dict[str, Any]:
    """
    Create the payload for the API request.
    
    Args:
        input_text (str): The input text for text generation.
    
    Returns:
        Dict[str, Any]: The payload for the API request.
    """
    return {
        "inputs": input_text,
        "parameters": {
            "max_new_tokens": MAX_NEW_TOKENS,
            "num_return_sequences": NUM_RETURN_SEQUENCES,
            "temperature": TEMPERATURE
        }
    }

def generate_text(input_text: str) -> str:
    """
    Generate text using the Hugging Face Inference API.
    
    Args:
        input_text (str): The input text for text generation.
    
    Returns:
        str: The generated text.
    
    Raises:
        requests.RequestException: If there's an error with the API request.
        ValueError: If the API response is not in the expected format.
    """
    api_key = get_api_key()
    headers = create_headers(api_key)
    payload = create_payload(input_text)

    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()
    output = response.json()
    
    if isinstance(output, list) and len(output) > 0 and 'generated_text' in output[0]:
        return output[0]['generated_text']
    else:
        raise ValueError("Unexpected API response format")

def main():
    """
    Main function to demonstrate text generation.
    """
    input_text = "Life is a box of"
    
    try:
        generated_text = generate_text(input_text)
        print(f"Input: {input_text}")
        print(f"Generated Text: {generated_text}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()