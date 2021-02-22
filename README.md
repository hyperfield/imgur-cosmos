# Space Imgur

This package contains a set of API scripts that do the following tasks:

- Download Hubble Telescope images by category through the corresponding API.
- Download latest Space X images through the corresponding API.
- Process the downloaded images by resizing them to images with the larger sides no greater than 1800 pixels; and to save them as JPEG if they are of a different format.
- Upload images to Imgur via its API.

## Installation

Python 3 should be already installed. If not, then please do so.

Now create a Python virtual environment:

    python3 -m venv .cosmos

Activate the environment, e.g.:

    source .cosmos/bin/activate

Install the required libraries:

    pip install -r requirements.txt

[Create an account](https://imgur.com) with Imgur and [register an application](https://api.imgur.com/oauth2/addclient) to get your `client-id` and `client-secret`. In the field `Authorization callback URL` you should specify `http://localhost`.

Now put the  `client-id` and `client-secret` that you just got into a newly created file `.env` which has to be in the **Space Imgur** directory.

Example of `.env`:

    IMGUR_CLIENT_ID='09f0d0001d54jkr'
    IMGUR_CLIENT_SEC='b83ddc23f32b1crb45ef1fe6a92af6ca24e5db83'


## Launching the scripts

To download Hubble images by category:

    python fetch_spacex.py

If you make the file executable by

    chmod +x fetch_spacex.py

then you can also launch directly, e.g.:

    ./fetch_spacex.py

The same principles apply to the scripts `fetch_hubble.py` and `imgur_upload`, but you can also run them with arguments:

    ./fetch_hubble.py spacecraft
    ./fetch_hubble.py news

The following are some of the available picture categories to fetch: `news`, `holiday_cards` (the default category in the script), `spacecraft`, `printshop`, `stsci_gallery`. Make sure there is no space after the comma if you enter more than one folder to upload as a command line argument to `imgur_upload.py`.

    ./imgur_upload.py images/hubble,images/hubble/adjusted
    ./imgur_upload.py ~/Pictures/Space

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).