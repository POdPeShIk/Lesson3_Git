from dotenv import load_dotenv
import argparse
import requests
import os


def shorten_link(token, url):
    headers = {"Authorization": f"Bearer {token}"}
    long_url = {"long_url": url}
    response = requests.post('https://api-ssl.bitly.com/v4/bitlinks',headers=headers,json=long_url)
    response.raise_for_status()
    return response.json()["id"]


def get_total_clicks(bitlink, token):
    service_url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
    headers = {"Authorization": f"Bearer {token}"}
    params = {
    'unit': "day",
    'units': -1
    }
    response = requests.get(service_url, headers=headers, params=params)
    response.raise_for_status()
    total_clicks = response.json()["total_clicks"]
    return total_clicks


def is_bitlink(bitlink, token):
    service_url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}'
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(service_url, headers=headers)
    return response.ok


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(
        description='Описание что делает программа'
    )
    parser.add_argument('urls', help='Ссылка', type=str)
    args = parser.parse_args()
    url = args.urls
    token = os.environ['BITLY_TOKEN']
    if is_bitlink(url, token):
        print(get_total_clicks(url, token))
    else:
        print(shorten_link(token, url))


if __name__ == "__main__":
    main()
