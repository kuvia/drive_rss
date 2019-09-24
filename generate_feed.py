#!/usr/bin/env python
# -*- coding: utf-8 -*-

# parsing
import requests
import re
import codecs
import json
from datetime import datetime
from datetime import timezone

# writing
from feedgen.feed import FeedGenerator

# cli
import sys
import argparse

parser = argparse.ArgumentParser(description='Generates a RSS Feed file from a Google Drive folder ID')
parser.add_argument('--folder', metavar='d', type=str, help='folder id from share link', required=True)
args = parser.parse_args()

# Decode function source: https://stackoverflow.com/a/24519338
ESCAPE_SEQUENCE_RE = re.compile(r'''
    ( \\U........      # 8-digit hex escapes
    | \\u....          # 4-digit hex escapes
    | \\x..            # 2-digit hex escapes
    | \\[0-7]{1,3}     # Octal escapes
    | \\N\{[^}]+\}     # Unicode characters by name
    | \\[\\'"abfnrtv]  # Single-character escapes
    )''', re.UNICODE | re.VERBOSE)

def decode_escapes(s):
    def decode_match(match):
        return codecs.decode(match.group(0), "unicode-escape")
    return ESCAPE_SEQUENCE_RE.sub(decode_match, s)

# TODO need to verify if it works with bigger folders
def parse(folder_id):
    r = requests.get("https://drive.google.com/drive/folders/%s"%folder_id)
    html = r.text
    # we back to parsing html with regex!
    title = re.search("<title>([^<]+) – Google", html).group(1)
    folder_link = "https://drive.google.com/drive/folders/%s"%folder_id
    matches = re.search("_DRIVE_ivd\\'[^']+'([^']+)",html)
    file_info = matches.group(1)
    file_info = decode_escapes(file_info)
    file_info_json = json.loads(file_info)
    items = []
    for i in file_info_json[0]:
        file_id = i[0]
        file_name = i[2]
        created_date = i[9]
        created_date = datetime.fromtimestamp(created_date/1000)
        created_date = created_date.replace(tzinfo=timezone.utc)
        direct_link = "https://drive.google.com/uc?export=download&id=%s"%file_id
        items.append({"id": file_id, "name": file_name, "created": created_date, "direct_link": direct_link})
    items = sorted(items, key=lambda x: x["created"])
    return {"title": title, "id": folder_id, "items": items, "folder_link": folder_link}

def create_feed(folder):
    fg = FeedGenerator()
    fg.load_extension("podcast")
    fg.title(folder["title"])
    fg.link(href=folder["folder_link"], rel="alternate")
    fg.subtitle("Auto-generated feed from a Drive folder")
    for item in folder["items"]:
        fe = fg.add_entry()
        fe.id(item["direct_link"])
        fe.title(item["name"])
        fe.enclosure(item["direct_link"], 0, 'audio/mpeg')
        fe.pubDate(item["created"])
    fg.rss_str(pretty=True)
    fg.rss_file("%s.xml"%folder["title"])

folder = parse(args.folder)
create_feed(folder)
