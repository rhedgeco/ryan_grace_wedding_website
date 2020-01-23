import falcon

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
        if not validate_params(req.params, 'images_per_page', 'page_number'):
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.body = 'Bad Parameters.'
            return

        images_per_page = int(req.params['images_per_page'])
        page_number = int(req.params['page_number'])

        image_path = self.path / 'images/full'
        images = [f for f in sorted(listdir(image_path)) if isfile(join(image_path, f))]  # gets files in a directory
        index_start = max(0, min(images_per_page * (page_number - 1), len(images)))
        index_end = max(0, min(images_per_page * page_number, len(images)))
        images = images[index_start:index_end]  # prune list to size

        html_path = self.path / 'html/image.html'
        image_html = ''
        with open(html_path, 'r') as f:
            image_html = f.read()

        frontend_image_path = image_path.relative_to('frontend')
        gallery_html = ''
        for image in images:
            gallery_html += image_html.replace('[img]', str(frontend_image_path / image))
        resp.body = gallery_html
