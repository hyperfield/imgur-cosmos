#!/usr/bin/env python3

import requests
import urllib3
from helpers import get_filename_ext, fetch_image, adjust_picture
import argparse


def fetch_img_versions(img_id):
    api_url = "http://hubblesite.org/api/v3/image"
    response = requests.get(f'{api_url}/{img_id}')
    response.raise_for_status()
    img_list = response.json()['image_files']
    for img in img_list:
        print(f'https:{img["file_url"]}')


def fetch_hubble_picture_by_id(img_id, folder="images/hubble"):
    api_base_url = "http://hubblesite.org/api/v3/image/"
    response = requests.get(f"{api_base_url}{img_id}")
    try:
        picture = response.json()['image_files'][-2]['file_url']
    except IndexError:
        picture = response.json()['image_files'][-1]['file_url']
    img_url = f"http:{picture}"
    file_ext = get_filename_ext(img_url)[1]
    filename = f"{img_id}.{file_ext}"
    fetch_image(img_url, filename, folder)

    return filename


def fetch_hubble_pictures_by_category(collection_name="holiday_cards"):
    url_template = "http://hubblesite.org/api/v3/images"
    payload = {"collection_name": collection_name}
    response = requests.get(url_template, params=payload)
    id_dicts = response.json()
    id_list = [id_dict['id'] for id_dict in id_dicts]
    file_list = []
    for img_id in id_list:
        print(f'Fetching image id {img_id}...')
        file_list.append(fetch_hubble_picture_by_id(img_id))
    return file_list


def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    parser = argparse.ArgumentParser(
        description="""This script fetches image files from the Hubble website
                       to your computer."""
                    )
    parser.add_argument('collection_name',
                        help='The name of the photo set at Hubble.',
                        nargs='?', type=str)
    args = parser.parse_args()
    folder = 'images/hubble'
    img_files = fetch_hubble_pictures_by_category(args.collection_name)
    for img_file in img_files:
        adjust_picture(f"{folder}/{img_file}")


if __name__ == "__main__":
    main()
