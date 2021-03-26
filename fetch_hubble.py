#!/usr/bin/env python3

import argparse
import logging
from pathlib import Path
from requests.models import HTTPError
import requests
import urllib3

from helpers import extract_file_ext, fetch_image


def fetch_hubble_picture_by_id(img_id, folder="images/hubble"):
    api_base_url = "http://hubblesite.org/api/v3/image/"
    try:
        response = requests.get(f"{api_base_url}{img_id}")
        response.raise_for_status()
        try:
            picture = response.json()['image_files'][-2]['file_url']
        except IndexError:
            picture = response.json()['image_files'][-1]['file_url']
        img_url = f"http:{picture}"
        file_ext = extract_file_ext(img_url)[1]
        filename = f"{img_id}{file_ext}"
        fetch_image(img_url, filename, folder)
        return filename

    except HTTPError:
        print(f"Error {response.status_code}")
        return None


def fetch_hubble_pictures_by_category(collection_name="holiday_cards"):
    url_template = "http://hubblesite.org/api/v3/images"
    payload = {"collection_name": collection_name}
    try:
        response = requests.get(url_template, params=payload)
        response.raise_for_status()
        json_img_ids = response.json()
        img_ids = [json_img_id['id'] for json_img_id in json_img_ids]
        files = []
        for img_id in img_ids:
            logging.info(f'fetch_hubble_pictures_by_category(): Fetching image id {img_id}...')
            files.append(fetch_hubble_picture_by_id(img_id))
        return files
    except HTTPError:
        print(f"Error {response.status_code}")
        return None


def main():
    logging.basicConfig(format='%(asctime)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S',
                        filename="info.log", level=logging.INFO)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    parser = argparse.ArgumentParser(
        description="""This script fetches image files from the Hubble website
                       to your computer."""
                    )
    parser.add_argument('collection_name',
                        help='The name of the photo set at Hubble.',
                        nargs='?', type=str)
    args = parser.parse_args()
    folder = "images/hubble"
    Path(folder).mkdir(parents=True, exist_ok=True)
    fetch_hubble_pictures_by_category(args.collection_name)


if __name__ == "__main__":
    main()
