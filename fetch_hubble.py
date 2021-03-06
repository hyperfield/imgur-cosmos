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


def fetch_hubble_pictures_by_category(collection_name="holiday_cards"):
    url_template = "http://hubblesite.org/api/v3/images"
    payload = {"collection_name": collection_name}
    response = requests.get(url_template, params=payload)
    response.raise_for_status()
    img_ids_and_names = response.json()
    img_ids = [json_img_id['id'] for json_img_id in img_ids_and_names]
    files = []
    for img_id in img_ids:
        logging.info(f'fetch_hubble_pictures_by_category(): Fetching image id {img_id}...')
        try:
            files.append(fetch_hubble_picture_by_id(img_id))
        except HTTPError as error:
            print(f"Error {error}")
    return files


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
    try:
        fetch_hubble_pictures_by_category(args.collection_name)
    except HTTPError as error:
        print(f"Error {error}")


if __name__ == "__main__":
    main()
