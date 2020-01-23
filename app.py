from general_falcon_webserver.backend.general_manager.app_constructor import WebApp

from backend.gallery_info import GalleryInfo
from backend.gallery_resource import GalleryHtmlImages

app = WebApp(frontend_dir='frontend', page_404='page404.html')

gallery = GalleryHtmlImages('frontend/data/images/gallery')
app.add_route('gallery_html_images', gallery)

gallery_info = GalleryInfo('frontend/data/images/gallery')
app.add_route('gallery_info', gallery_info)

app.launch_webserver(port=6009)
