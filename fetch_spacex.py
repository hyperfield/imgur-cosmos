#!/usr/bin/env python3

import requests
from requests.models import HTTPError
from helpers import fetch_image


def fetch_spacex_last_launch():
    api_url = "https://api.spacexdata.com/v4/launches/latest"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        pictures = response.json()['links']['flickr']['original']
        for picture_number, picture in enumerate(pictures):
            file_name = f"spacex{picture_number+1}.jpg"
            fetch_image(picture, file_name, 'images/spacex')
    except HTTPError:
        print(f"Error {response.status_code}")


def main():
    fetch_spacex_last_launch()


if __name__ == "__main__":
    main()
