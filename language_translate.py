import os
# from dotenv import load_dotenv
import openai
import json

# load_dotenv()

# Set the API key
openai.api_key = os.getenv("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")

# Rest of your code
personal_details = {
    "Name": "Sagar Mishra",
    "Age": "24",
    "Occupation": "Software Developer",
    "Location": "Kathmandu",
    "Hobbies": [
        {
            "title": "Watching Movies"
        },
        {
            "title": "Reading Books"
        }
    ]
}

# Convert the dictionary to a JSON string
text_to_translate = json.dumps(personal_details, indent=4)
language = 'Nepali'

# Create a translation prompt that includes both keys and values
translation_prompt = f"Translate the following English text to {language}:\n{text_to_translate}"

# Now you can use the API key to make requests
response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=translation_prompt,
    max_tokens=50
)

translated_text = response.choices[0].text.strip()
print(translated_text)
