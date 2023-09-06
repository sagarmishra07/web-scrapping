import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("OPENAI_KEY")

api_url = 'https://api.openai.com/v1/engines/davinci-codex/completions'

with open('data.json', 'r') as file:
    data = json.load(file)

# Extract organization data
organizations = data

# Construct a query that includes organization data
query = "Provide information about organizations with names starting with 'z':\n"

for org in organizations:
    org_name = org.get('Organization Name', 'N/A')
    reg_no = org.get('Reg. No', 'N/A')
    vat_no = org.get('Vat No', 'N/A')
    address = org.get('Address', 'N/A')
    country = org.get('Country', 'N/A')
    website_url = org.get('Website URL', 'N/A')
    email = org.get('Email', 'N/A')
    telephone_number = org.get('Telephone number', 'N/A')
    mobile_number = org.get('Mobile number', 'N/A')
    fax = org.get('Fax', 'N/A')
    po_box = org.get('PO Box', 'N/A')
    key_person = org.get('Key Person', 'N/A')
    establishment_date = org.get('Establishment Date', 'N/A')

    query += f"- Organization Name: {org_name}\n"
    query += f"  Registration No: {reg_no}\n"
    query += f"  Vat No: {vat_no}\n"
    query += f"  Address: {address}\n"
    query += f"  Country: {country}\n"
    query += f"  Website URL: {website_url}\n"
    query += f"  Email: {email}\n"
    query += f"  Telephone number: {telephone_number}\n"
    query += f"  Mobile number: {mobile_number}\n"
    query += f"  Fax: {fax}\n"
    query += f"  PO Box: {po_box}\n"
    query += f"  Key Person: {key_person}\n"
    query += f"  Establishment Date: {establishment_date}\n\n"

# Create the request
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json',
}

data = {
    'prompt': query,
    'max_tokens': 500  # Adjust the max_tokens as needed
}

# Send the request to the ChatGPT API
response = requests.post(api_url, headers=headers, json=data)

if response.status_code == 200:
    # Process the response from the API
    result = response.json()
    generated_response = result['choices'][0]['text']
    print(generated_response)
else:
    # Handle API errors
    print(f"Error: {response.status_code}")
