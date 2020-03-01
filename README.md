# Google Drive folder to Podcast RSS

A small Python script that generates a RSS feed ready to be consumed by a Podcast player from a publicly shared Google Drive folder. I use it to periodically call it and put the resulting file on a small webhost to have my personalized Podcast feed.

Items are currently sorted so the latest changed files appear at the top.

## Installation

Create a Python 3 virtual environment:

    python3 -m venv venv

Activate the virtual environment:

    source venv/bin/activate

Install requirements:

    pip install -r requirements.txt

Create a Google API key:

https://console.developers.google.com

- Create a project first https://console.developers.google.com/projectcreate
- Within your project click on Dashboard in the menu, click Enable APIs and Services and select Google Drive API and click Enable
- Within your project, click on Credentials in the menu, Create Credentials and select API key
- This API key will be used when running the script

## Usage

- The Google Drive folder needs to be publicly visible
- Your share url should look something like this: https://drive.google.com/drive/folders/SOME_LONG_ID


    python generate_feed.py --folder SOME_LONG_ID --apikey YOUR_API_KEY

The script will create a XML file named after your folder for easier typing into the Podcast player of your choice.
