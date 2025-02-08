import os
import json
import httpx
from bs4 import BeautifulSoup
from typing import List
from pathlib import Path
from httpx import HTTPError
from fasthtml.common import *
from fasthtml.svg import Svg
from fasthtml.svg import Path as SPath

# Constants
FOLDER_NAME = Path.cwd()/".fh-heroicons"

def icon_url(icon_name: str, variant: str):
    return f"https://raw.githubusercontent.com/tailwindlabs/heroicons/refs/heads/master/src/24/{variant}/{icon_name}.svg"

def path_attrs(svg_str: str) -> List[dict]:
    soup = BeautifulSoup(svg_str, 'lxml')
    paths = soup.find_all('path')
    attrs_list = [dict(path.attrs) for path in paths]
    
    # Replace hardcoded colors with currentColor
    for attrs in attrs_list:
        if 'fill' in attrs and attrs['fill'].startswith('#'):
            attrs['fill'] = 'currentColor'
        if 'stroke' in attrs and attrs['stroke'].startswith('#'):
            attrs['stroke'] = 'currentColor'
            
    return attrs_list

def check_cache(icon_name, variant, folder=None):
    folder = folder or FOLDER_NAME
    if not os.path.exists(folder): os.mkdir(folder) 

    if f"{icon_name}_{variant}" in os.listdir(folder):
        return True
    return False

def save_icon_data(icon_name, path_attrs_list, variant):
    with open(os.path.join(FOLDER_NAME, f"{icon_name}_{variant}"), 'w') as f:
        json.dump(path_attrs_list, f)

def read_icon_data(icon_name, variant):
    with open(os.path.join(FOLDER_NAME, f"{icon_name}_{variant}"), 'r') as f:
        return json.load(f)

def get_icon_data(icon_name, variant): 
    if check_cache(icon_name, variant):
        icon_data = read_icon_data(icon_name, variant=variant)
    else: 
        p_url = icon_url(icon_name, variant=variant)

        r = httpx.get(p_url)
        if r.status_code == 200:
            icon_data = path_attrs(r.text)
            save_icon_data(icon_name, icon_data, variant=variant) #save it to cache
        else: 
            raise HTTPError(f"Getting icon data failed with status code: {r.status_code}")

    return icon_data

def Heroicon(icon_str: str, cls=None, style=None, size: int = 24, variant: str = "outline") -> FT:
    assert variant in ["solid", "outline"], "Only `solid` or `outline` variants are supported"
    assert size > 0, "size must be positive"

    pas = get_icon_data(icon_str, variant=variant)

    icon = Svg(cls=cls, style=style, width=size, height=size, viewBox="0 0 24 24", fill="none", xmlns="http://www.w3.org/2000/svg")(
        *[SPath(**pa) for pa in pas]
    )
    return icon