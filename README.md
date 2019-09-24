# Google Drive folder to Podcast RSS

A small Python script that generates a RSS feed ready to be consumed by a Podcast player from a publicly shared Google Drive folder. I use it to periodically call it and put the resulting file on a small webhost to have my personalized Podcast feed.

## Installation

Create a Python 3 virtual environment:

    python3 -m venv venv

Activate the virtual environment:

    source venv/bin/activate

Install requirements:

    pip install -r requirements.txt

## Usage

- The Google Drive folder needs to be publicly visible
- Your share url should look something like this: https://drive.google.com/drive/folders/SOME_LONG_ID


    python generate_feed.py --folder SOME_LONG_ID

The script will create a XML file named after your folder for easier typing into the Podcast player of your choice.
