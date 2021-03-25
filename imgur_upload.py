#!/usr/bin/env python3

import argparse
from datetime import datetime
from os import getenv
from os import listdir
from dotenv import load_dotenv
import logging
from os import path
from pathlib import Path

from helpers import authenticate, adjust_picture
import imgurpython


def upload_img(client, img_path, name="Space", title="Space picture"):
    # Metadata for the upload. All of these are optional, including
    # this config dict itself.
    album = "Space images"  # You can also enter an album ID here
    config = {
        'album': album,
        'name':  name,
        'title': title,
        'description': 'A space image uploaded on {0}'.format(datetime.now())
    }

    logging.info(f"upload_img(): Uploading image {img_path}...")
    image = client.upload_from_path(img_path, config=config, anon=False)

    return image


def main():
    logging.basicConfig(format='%(asctime)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S',
                        filename="info.log", level=logging.INFO)
    default_folder_paths = "images/hubble/,images/spacex/"
    parser = argparse.ArgumentParser(
        description="""This script uploads image files to Imgur."""
        )
    parser.add_argument('folder_paths',
                        help='Comma-delimited list of folder(s) with image files to upload',
                        default=default_folder_paths, nargs='?', type=str)
    args = parser.parse_args()
    args.folder_paths = [item.strip() for item in args.folder_paths.split(',')]
    file_listings = {folder: listdir(folder) for folder in args.folder_paths}

    load_dotenv()
    client_id = getenv('IMGUR_CLIENT_ID')
    client_secret = getenv('IMGUR_CLIENT_SEC')

    client = authenticate(client_id, client_secret)

    for folder, file_listing in file_listings.items():
        for filename in file_listing:
            file_path = path.join(f"{folder}", f"{filename}")
            if not Path(file_path).is_file():
                continue

            adjust_picture(file_path)
            try:
                if "spacex" in filename:
                    upload_img(client, file_path,
                                name="SpaceX",
                                title="SpaceX image")
                    continue

                upload_img(client, file_path,
                            name="Hubble",
                            title="Hubble image")

            except imgurpython.helpers.error.ImgurClientError:
                logging.info(f"imgur_upload.py: main(): Could not upload {filename}, some Imgur error occurred.")


if __name__ == '__main__':
    main()
