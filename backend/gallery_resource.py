import falcon
import base64

from pathlib import Path
from os import listdir
from os.path import isfile, join

from backend.api_utils import validate_params


class GalleryHtmlImages:

    def __init__(self, gallery_path: str):
        self.path = Path(gallery_path)
        if not self.path.exists():
            print(f'warning {self.path} does not exist')

    def on_get(self, req, resp):
        if not validate_params(req.params, 'page_number'):
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.body = 'Bad Parameters.'
            return

        images_per_page = 10
        page_number = int(req.params['page_number'])

        image_path = self.path / 'images'
        image_tiny_path = image_path / 'tiny'
        image_full_path = image_path / 'full'
        images = [f for f in sorted(listdir(image_full_path)) if
                  isfile(join(image_full_path, f))]  # gets files in a directory
        index_start = max(0, min(images_per_page * (page_number - 1), len(images)))
        index_end = max(0, min(images_per_page * page_number, len(images)))
        images = images[index_start:index_end]  # prune list to size

        html_path = self.path / 'html' / 'image.html'
        image_html = ''
        with open(html_path, 'r') as f:
            image_html = f.read()

        frontend_image_path = image_full_path.relative_to('frontend')
        gallery_html = ''
        for image in images:
            with open(image_full_path / image, 'rb') as image_file:
                encoded_string = str(base64.b64encode(image_file.read()))[:-1].replace('b\'', '')
            gallery_html += image_html \
                .replace('[img-thumb]', 'data:image/jpg;base64,' + encoded_string) \
                .replace('[img-full]', str(frontend_image_path / image))
        resp.body = gallery_html
