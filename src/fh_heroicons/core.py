from fasthtml.common import *
from fasthtml.svg import Svg
from fasthtml.svg import Path as SPath
import httpx
from httpx import HTTPError
import os 
from pathlib import Path

def icon_url(icon_name: str):
    return f"https://raw.githubusercontent.com/tailwindlabs/heroicons/refs/heads/master/src/24/outline/{icon_name}.svg"
def path_d(svg_str: str):
    pattern = r'd="(.*?)" '
    finds = re.findall(pattern=pattern, string=svg_str)
    assert len(finds) == 1
    return finds[0]

def get_icon_data(icon_str: str):
    p_url = icon_url(icon_str)
    r = httpx.get(p_url)
    if r.status_code == 200:
        return path_d(r.text)
    else: 
        raise HTTPError(f"Getting icon data failed with status code: {r.status_code}")

cwd = Path.cwd()

FOLDER_NAME = cwd/".fh-heroicons"

def check_cache(icon_name, folder=None):
    folder = folder or FOLDER_NAME
    if not os.path.exists(folder): os.mkdir(folder) 

    if icon_name in os.listdir(folder):
        return True
    return False

def save_icon_data(icon_name, icon_data):
    with open(os.path.join(FOLDER_NAME, icon_name), 'w') as f:
        f.write(icon_data)

def read_icon_data(icon_name):
    with open(os.path.join(FOLDER_NAME, icon_name), 'r') as f:
        icon_data = f.read()
    return icon_data

def get_icon_data(icon_name): 
    if check_cache(icon_name):
        icon_data = read_icon_data(icon_name)
    else: 
        p_url = icon_url(icon_name)
        r = httpx.get(p_url)
        if r.status_code == 200:
            icon_data = path_d(r.text)
            save_icon_data(icon_name, icon_data) #save it to cache
        else: 
            raise HTTPError(f"Getting icon data failed with status code: {r.status_code}")

    return icon_data

def Heroicon(icon_str: str, cls=None, style=None, size: int = 24) -> FT:
    pd = get_icon_data(icon_str)

    icon = Svg(cls=cls, style=style, width=size, height=size, viewBox="0 0 24 24", fill="none", xmlns="http://www.w3.org/2000/svg")(
        SPath(d=pd, stroke="currentColor", stroke_width="1.5", stroke_linecap="round", stroke_linejoin="round")
    )
    return icon