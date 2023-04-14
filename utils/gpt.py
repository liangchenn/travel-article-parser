import re
import os
import json

import dotenv
import openai

from utils.cache import local_cache

# load env
dotenv.load_dotenv()
# load API key
openai.api_key = os.getenv("OPENAI_API_KEY")


PROMPT = """
I will provide you a list of travel locations separated by comma `,`
Your tasks is to tell me which locations are mentioned and remove non location words.

The answer format should be a list of location names. 
Please use `[]` to include those locations, and use comma `, ` to separate the locations you found.
For example, `[Shibuya Skytree, Taipei 101, Tokyo Station]`.
Please notice that the length of location name won't exceed 30 character, 
remember to remove the invalid ones. And always remember to return locations instead of a whole sentence.

The list:

"""


def split_text(text, max_tokens):
    tokenized_text = " ".split(text)
    if len(tokenized_text) <= max_tokens:
        return [text]

    paragraphs = text.split("\n")
    chunks = []

    current_chunk = ""
    for paragraph in paragraphs:
        if len(current_chunk) + len(paragraph) < max_tokens:
            current_chunk += "\n" + paragraph
        else:
            chunks.append(current_chunk.strip())
            current_chunk = paragraph

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

@local_cache
def process_text_with_gpt(prompt, model="gpt-3.5-turbo", max_tokens=3000, max_output=400):
    max_tokens = 3000
    chunks = split_text(prompt, max_tokens - 10)

    results = []
    for chunk in chunks:
        
        response = openai.ChatCompletion.create(
            model=model,
            max_tokens=max_output,
            temperature=0.5,
            messages=[{"role": "user", "content": chunk}]
        )
        results.append(response.choices[0]['message']['content'].strip())

    return "\n".join(results)