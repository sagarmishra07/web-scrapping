import requests
from lxml import html
import json


def get_request(url):
    response = requests.get(url)
    page_content = response.content
    tree = html.fromstring(page_content)
    return tree


def extract_member_details(url):
    response = get_request(url)
    details_elements = response.xpath('//ul[@class="list-group small"]/li[@class="list-group-item"]')
    member_details = {}

    for element in details_elements:
        text = element.text_content().strip()
        key, value = text.split(':', 1)  # Split the text at the first ':' character
        member_details[key.strip()] = value.strip()

    return member_details


def extract_members():
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                'u',
                'v', 'w', 'x', 'y', 'z']

    member_details_list = []

    for data in alphabet:

        response = get_request(f'https://www.taan.org.np/members?l={data}')
        xpath_expression = '/html/body/div[1]/div[2]/div/div/div[2]'
        member_links = response.xpath(xpath_expression + '//a/@href')

        for link in member_links:
            if link.startswith('http'):
                member_details = extract_member_details(link)
                member_details_list.append(member_details)
                save_to_json(member_details_list)

    return member_details_list


def save_to_json(member_details_list):
    with open('data.json', 'w', encoding='utf-8') as json_file:
        json.dump(member_details_list, json_file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    members = extract_members()
