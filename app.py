from general_falcon_webserver.backend.general_manager.app_constructor import WebApp

app = WebApp(frontend_dir='frontend', page_404='page404.html')

app.launch_webserver()
