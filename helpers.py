from PIL import Image
import logging
from pathlib import Path
from os import path
import requests
from PIL import UnidentifiedImageError

from imgurpython import ImgurClient


def extract_filename_ext(url):
    filename_ext = path.splitext(path.basename(url))
    return filename_ext


def fetch_image(img_url, file_name, folder='images/'):
    file_path = path.join(folder, file_name)
    if Path(file_path).is_file():
        logging.info(f"fetch_image(): {file_path} already exists, not fetching it")
        return file_path

    img_response = requests.get(img_url, verify=False)
    img_response.raise_for_status()
    with open(file_path, 'wb') as file:
        file.write(img_response.content)
    return file_path


def adjust_picture(picture_file_path):
    max_side_px = 1800
    file_name, file_extention = extract_filename_ext(picture_file_path)
    file_name_and_ext = f"{file_name}.{file_extention}"
    try:
        image = Image.open(picture_file_path)
        save_path = f"{picture_file_path[0: -len(file_name_and_ext)]} adjusted"
        Path(save_path).mkdir(parents=True, exist_ok=True)
        file_save_path = path.join(save_path, f'{file_name}.jpg')
        image_size = image.size
        larger_side_index = image_size[0] < image_size[1]
        if image.mode == "RGBA":
            logging.info(f"adjust_picture(): Convertitng {file_name_and_ext} mode to RGB from RGBA")
            image = image.convert("RGB")
        if image_size[larger_side_index] > max_side_px:
            logging.info(f"adjust_picture(): Resizing {file_name_and_ext}, saving as JPEG")
            image.thumbnail([max_side_px, max_side_px])
            image.save(file_save_path, format="JPEG")
        elif image.format != "JPEG":
            logging.info(f"adjust_picture(): Converting {file_name_and_ext} to JPEG")
            image.save(file_save_path, format="JPEG")
    except UnidentifiedImageError:
        logging.info(f"adjust_picture(): {file_name_and_ext} does not seem to be an image file")


def authenticate(client_id, client_secret):

    client = ImgurClient(client_id, client_secret)
    authorization_url = client.get_auth_url('pin')

    print("Go to the following URL: {0}".format(authorization_url))

    pin = input("Enter pin code: ")

    credentials = client.authorize(pin, 'pin')
    client.set_user_auth(credentials['access_token'],
                         credentials['refresh_token'])

    return client
