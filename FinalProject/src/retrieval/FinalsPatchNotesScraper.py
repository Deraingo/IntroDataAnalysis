import requests
from urllib import robotparser
from bs4 import BeautifulSoup
import re

root_url = 'https://www.reachthefinals.com/'
rp = robotparser.RobotFileParser()
rp.set_url(root_url + "robots.txt")
rp.read()

def isAllowedToScrape(url):
    return rp.can_fetch("*", url)

def scrape_patch_notes(version_num):
    url = f"{root_url}patchnotes/{version_num}"
    if not isAllowedToScrape(url):
        print(f"Skipping {url}, it is not allowed by robots.txt")
        return None
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.get_text(separator='\n')
        return content
    else:
        print(f"Failed to retrieve {url}, status code: {response.status_code}")
        return None

def save_to_file(content, version_str):
    filename = f"patchnotes_v{version_str}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Saved patch notes for version {version_str} to {filename}")

for major in range(1, 5):
    for minor in range(0, 10):
        for patch in range(0, 10):
            version_str = f"{major}.{minor}.{patch}"
            version_num = f"{major}{minor}{patch}"
            print(f"Scraping patch notes for version {version_str} at /patchnotes/{version_num}")
            content = scrape_patch_notes(version_num)
            if content:
                save_to_file("../../PathNotes/" + content, version_str)
