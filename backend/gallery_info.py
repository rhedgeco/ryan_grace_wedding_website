import falcon
import json
import math

from pathlib import Path
from os import listdir
from os.path import isfile, join


class GalleryInfo:

    def __init__(self, gallery_path: str):
        self.path = Path(gallery_path)
        if not self.path.exists():
            print(f'warning {self.path} does not exist')

    def on_get(self, req, resp):
        image_path = self.path / 'images/full'
        images = [f for f in sorted(listdir(image_path)) if isfile(join(image_path, f))]  # gets files in a directory

        info = {
            'image_count': len(images),
            'images_per_page': 10,
            'page_count': int(math.ceil(len(images) / 10.0))
        }

        resp.body = json.dumps(info, ensure_ascii=True)
