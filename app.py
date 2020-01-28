from argparse import ArgumentParser
from pathlib import Path

from general_falcon_webserver.backend.general_manager.databases import SqliteDatabase
from general_falcon_webserver.backend.general_manager.app_constructor import WebApp

from backend.admins import Admins
from backend.authenticator import Auth
from backend.gallery_info import GalleryInfo
from backend.gallery_resource import GalleryHtmlImages
from backend.myregistry_scraper import MyRegistryScraper


def parse_args():
    parser = ArgumentParser(description="Website for Grace and Ryan's Wedding!")
    parser.add_argument("--port", type=int, default=80, help="Port to host server.")
    parsed_args = parser.parse_args()
    return parsed_args


def configure_app():
    web_app = WebApp(frontend_dir='frontend', page_404='page404.html')

    with open(Path('backend') / 'database_setup.sql') as file:
        db_config = file.read()
    db = SqliteDatabase('wedding_db', db_config)

    gallery = GalleryHtmlImages('frontend/data/images/gallery')
    web_app.add_route('gallery_html_images', gallery)

    gallery_info = GalleryInfo('frontend/data/images/gallery')
    web_app.add_route('gallery_info', gallery_info)

    auth = Auth(db)
    web_app.add_route('auth', auth)

    admins = Admins(db)
    web_app.add_route('admins', admins)

    registry = MyRegistryScraper()
    web_app.add_route('myregistry_scraper', registry)

    return web_app


if __name__ == '__main__':
    args = parse_args()
    app = configure_app()
    app.launch_webserver(port=args.port)
