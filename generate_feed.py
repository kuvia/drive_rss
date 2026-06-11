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
import click

def parse(folder_id, api_key):
    folder_url = "https://www.googleapis.com/drive/v3/files/%s?key=%s"%(folder_id, api_key)
    r = requests.get(folder_url)
    folder = r.json()
    items, next_page_token = get_page(folder_id, api_key, None)
    while next_page_token != None:
        current_page, next_page_token = get_page(folder_id, api_key, next_page_token)
        items.extend(current_page)
    items = sorted(items, key=lambda x: x["created"])
    folder_link = "https://drive.google.com/drive/folders/%s"%folder_id
    return {"title": folder["name"], "id": folder_id, "items": items, "folder_link": folder_link}

def get_page(folder_id, api_key, next_page_token):
    params = {"q": "'%s' in parents and trashed=false and mimeType != 'application/vnd.google-apps.folder'"%folder_id, "key": api_key, "fields": "files(id,name,mimeType,createdTime,size,fileExtension),nextPageToken,incompleteSearch", "pageSize": 100}
    if next_page_token != None:
      params["pageToken"] = next_page_token
    url = "https://www.googleapis.com/drive/v3/files"
    r = requests.get(url, params=params)
    files = r.json()
    items = []
    for f in files["files"]:
        direct_link = "https://drive.google.com/uc?export=download&id=%s"%f["id"]
        date_string = f["createdTime"].replace("T", " ").replace("Z", "+00:00")
        created_date = datetime.fromisoformat(date_string)
        item = {"id": f["id"], "name": f["name"], "size": f["size"], "type": f["mimeType"], "created": created_date, "direct_link": direct_link}
        items.append(item)
    next_page_token = files["nextPageToken"] if "nextPageToken" in files else None
    return items, next_page_token


def create_feed(folder):
    fg = FeedGenerator()
    fg.load_extension("podcast")
    fg.title(folder["title"])
    fg.link(href=folder["folder_link"], rel="alternate")
    fg.subtitle("Auto-generated feed from a Drive folder")
    for item in folder["items"]:
        # check if 'size' key exists before using it
        if item["size"] is not None:
            fe = fg.add_entry()
            fe.id(item["direct_link"])
            fe.title(item["name"])
            fe.enclosure(item["direct_link"], str(item["size"]), item["type"])
            fe.pubDate(item["created"])
    fg.rss_file("%s.xml"%folder["title"], pretty=True)

@click.command()
@click.option('--folder', help='folder id from share link')
@click.option('--apikey', help='Google API key')
def main(folder, apikey):
    folder_data = parse(folder, apikey)
    create_feed(folder_data)

if __name__ == '__main__':
    main()
