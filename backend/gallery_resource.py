import falcon

from pathlib import Path
from os import listdir
from os.path import isfile, join

from backend.api_utils import validate_params


class GalleryHtmlImages:

    def __init__(self, gallery_path: str):
        self.path = Path(gallery_path).absolute()
        if not self.path.exists():
            print(f'warning {self.path} does not exist')

    def on_get(self, req, resp):
        if not validate_params(req.params, 'imageCount'):
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.body = 'Bad Parameters.'
            return

        image_count = int(req.params['imageCount'])

        image_path = self.path / 'images/tiny'
        images = [f for f in sorted(listdir(image_path)) if isfile(join(image_path, f))]  # gets files in a directory
        images = images[:image_count]  # prune list to size

        html_path = self.path / 'html/image.html'
        image_html = ''
        with open(html_path, 'r') as f:
            image_html = f.read()

        frontend_image_path = (image_path.relative_to(Path.cwd() / 'frontend'))
        gallery_html = ''
        for image in images:
            gallery_html += image_html.replace('[img]', str(frontend_image_path / image))
        resp.body = gallery_html
