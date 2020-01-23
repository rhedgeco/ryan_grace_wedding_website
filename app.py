from pathlib import Path

from general_falcon_webserver.backend.general_manager.databases import SqliteDatabase
from general_falcon_webserver.backend.general_manager.app_constructor import WebApp

from backend.admins import Admins
from backend.gallery_info import GalleryInfo
from backend.gallery_resource import GalleryHtmlImages

app = WebApp(frontend_dir='frontend', page_404='page404.html')

with open(Path('backend') / 'database_setup.sql') as file:
    db_config = file.read()
db = SqliteDatabase('wedding_db', db_config)

gallery = GalleryHtmlImages('frontend/data/images/gallery')
app.add_route('gallery_html_images', gallery)

gallery_info = GalleryInfo('frontend/data/images/gallery')
app.add_route('gallery_info', gallery_info)

admins = Admins(db)
app.add_route('admins', admins)

app.launch_webserver()
