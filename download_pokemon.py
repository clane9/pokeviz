"""Download all pokemon thumbnails from fandom wiki.

Thanks gpt :)
"""

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Base URL for the wiki
base_url = "https://goofy-legends-gl.fandom.com"
all_pages_url = f"{base_url}/wiki/Special:AllPages"

# Directory to save the downloaded images
save_dir = "pokemon"
os.makedirs(save_dir, exist_ok=True)


def get_pokemon_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.select("ul.mw-allpages-chunk li a")
    return [urljoin(base_url, link["href"]) for link in links]


def get_image_url(pokemon_url):
    response = requests.get(pokemon_url)
    soup = BeautifulSoup(response.text, "html.parser")
    img_tag = soup.select_one('img.thumbimage[data-image-name^="Shuffle"]')
    if img_tag:
        src = img_tag["src"]
        # Modify URL to get original resolution
        return src.split("/revision")[0]
    return None


def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Downloaded: {url} {filename}")
    else:
        print(f"Failed to download: {url}")


# Main execution
pokemon_links = get_pokemon_links(all_pages_url)

for link in pokemon_links:
    print(f"Link: {link}")
    image_url = get_image_url(link)
    if image_url:
        basename = f"{os.path.basename(link)}.png"
        filename = os.path.join(save_dir, basename)
        download_image(image_url, filename)

print("Download complete!")
