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

## Usage

- The Google Drive folder needs to be publicly visible
- Your share url should look something like this: https://drive.google.com/drive/folders/SOME_LONG_ID


    python generate_feed.py --folder SOME_LONG_ID

The script will create a XML file named after your folder for easier typing into the Podcast player of your choice.

## Disclaimer

This script makes do without using any Google APIs or SDKs because setting it up properly is a pain (you need approved OAuth client credentials even though you're only accessing publicly shared folders). The simplicity means you can use this out of the box but the HTML structure of a GDrive folder page might change completely overnight and break everything. Feel free to report issues or suggest how to do this in a better way!
