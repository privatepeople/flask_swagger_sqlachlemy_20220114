from flask import Flask

def created_app(config_name):
    app = Flask(__name__)
    
    # 만들어진 앱에, (server>config>환경클래스) 환경설정 불러오기.
    app.config.from_object(f'server.config.{config_name}')
    
    return app