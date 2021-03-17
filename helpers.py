from pathlib import Path
from os import path
import requests
import logging
from PIL import Image
from PIL import UnidentifiedImageError
from imgurpython import ImgurClient

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(name)s: %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                    filename="info.log", level=logging.INFO)

def extract_file_ext(url):
    filename_ext = path.splitext(path.basename(url))
    return filename_ext


def fetch_image(img_url, file_name, folder='images/'):
    file_path = path.join(folder, file_name)
    if Path(file_path).is_file():
        logging.info(f"fetch_image(): {file_path} already exists, not fetching it")
        return file_path

    response_img = requests.get(img_url, verify=False)
    response_img.raise_for_status()
    with open(file_path, 'wb') as file:
        file.write(response_img.content)
    return file_path


def adjust_picture(picture_file_path):
    max_side_px = 1800
    filename_tuple = extract_file_ext(picture_file_path)
    filename = f"{filename_tuple[0]}.{filename_tuple[1]}"
    try:
        image = Image.open(picture_file_path)
        save_path = picture_file_path[0: -len(filename)] + "adjusted"
        Path(save_path).mkdir(parents=True, exist_ok=True)
        file_save_path = path.join(save_path, f'{filename_tuple[0]}.jpg')
        image_size = image.size
        larger_side_index = image_size[0] < image_size[1]
        if image.mode == "RGBA":
            logging.info(f"adjust_picture(): Convertitng {filename} mode to RGB from RGBA")
            image = image.convert("RGB")
        if image_size[larger_side_index] > max_side_px:
            logging.info(f"adjust_picture(): Resizing {filename}, saving as JPEG")
            image.thumbnail([image_size[larger_side_index],
                            image_size[larger_side_index]])
            image.save(file_save_path, format="JPEG")
        elif image.format != "JPEG":
            logging.info(f"adjust_picture(): Converting {filename} to JPEG")
            image.save(file_save_path, format="JPEG")
    except UnidentifiedImageError:
        logging.info(f"adjust_picture(): {filename} does not seem to be an image file")


def authenticate(client_id, client_secret):

    client = ImgurClient(client_id, client_secret)
    authorization_url = client.get_auth_url('pin')

    print("Go to the following URL: {0}".format(authorization_url))

    pin = input("Enter pin code: ")

    credentials = client.authorize(pin, 'pin')
    client.set_user_auth(credentials['access_token'],
                         credentials['refresh_token'])

    return client
