from pathlib import Path
from os import path, getenv
import requests
import urllib3
from PIL import Image
from PIL import UnidentifiedImageError
from dotenv import load_dotenv
from imgurpython import ImgurClient


def get_filename_ext(url):
    parsed = url.split("/")[-1].split(".")
    return (parsed[-2], parsed[-1])


def fetch_image(img_url, file_name, folder='images/'):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    file_path = path.join(folder, file_name)
    if not Path(file_path).is_file():
        Path(folder).mkdir(parents=True, exist_ok=True)
        response_img = requests.get(img_url, verify=False)
        response_img.raise_for_status()
        print(file_path)
        with open(file_path, 'wb') as file:
            file.write(response_img.content)
    else:
        print(f"{file_path} already exists, not fetching it\n")
    return file_path


def adjust_picture(picture_file_path):
    filename_tuple = get_filename_ext(picture_file_path)
    filename = f"{filename_tuple[0]}.{filename_tuple[1]}"
    try:
        image = Image.open(picture_file_path)
        save_path = picture_file_path[0: -len(filename)] + "adjusted"
        Path(save_path).mkdir(parents=True, exist_ok=True)
        file_save_path = path.join(save_path, f'{filename_tuple[0]}.jpg')
        image_size = image.size
        larger_side_index = image_size[0] < image_size[1]
        smaller_side_index = not larger_side_index
        if image.mode == "RGBA":
            print(f"Convertitng {filename} mode to RGB from RGBA")
            image = image.convert("RGB")
        if image_size[larger_side_index] > 1800:
            print(f"Resizing {filename}, saving as JPEG\n")
            new_size_list = [int(1800/image_size[larger_side_index] *
                             image_size[smaller_side_index])]
            new_size_list.insert(larger_side_index, 1800)
            image.thumbnail(new_size_list)
            image.save(file_save_path, format="JPEG")
        elif image.format != "JPEG":
            print(f"Converting {filename} to JPEG")
            image.save(file_save_path, format="JPEG")
    except UnidentifiedImageError:
        print(f"{filename} does not seem to be an image file")


def authenticate():
    load_dotenv()
    client_id = getenv('IMGUR_CLIENT_ID')
    client_secret = getenv('IMGUR_CLIENT_SEC')

    client = ImgurClient(client_id, client_secret)

    # Authorization flow, pin example (see docs for other auth types)
    authorization_url = client.get_auth_url('pin')

    print("Go to the following URL: {0}".format(authorization_url))

    # Read in the pin, handle Python 2 or 3 here.
    pin = input("Enter pin code: ")

    # ... redirect user to `authorization_url`, obtain pin (or code or token)
    credentials = client.authorize(pin, 'pin')
    client.set_user_auth(credentials['access_token'], credentials['refresh_token'])

    print("Authentication successful! Here are the details:")
    print("   Access token:  {0}".format(credentials['access_token']))
    print("   Refresh token: {0}".format(credentials['refresh_token']))

    return client
