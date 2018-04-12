# -*- coding:utf-8 -*-
from flask import Flask,request
from werkzeug.routing import BaseConverter
from os import path
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import *
from flask_babel import Babel,gettext as _
from flask_gravatar import Gravatar
from config import config
from flask_login import LoginManager,current_user
from flask_pagedown import PageDown
class RegexConverter(BaseConverter):
    def __init__(self,url_map,*items):
        super(RegexConverter,self).__init__(url_map)
        self.regex=items[0]

basedir = path.abspath(path.dirname(__file__))

babel = Babel()
bootstrap = Bootstrap()
login_manager=LoginManager()
pagedowm = PageDown()
login_manager.session_protection='strong'
login_manager.login_view='auth.login'
nav = Nav()
db = SQLAlchemy()
#manager = Manager()
nav.register_element('top',Navbar(u'flask入门',View(u'主页','main.index'),
                                                View(u'关于','main.about'),
                                                View(u'登陆','auth.login'),
                                                View(u'注册','auth.register'),
))

def create_app(config_name='production'):
    app = Flask(__name__)
    app.url_map.converters['regex'] = RegexConverter
    app.config.from_object(config[config_name])
    #app.config.from_pyfile('config')
    #app.secret_key='hard string for password'
    #app.config.from_pyfile('babel.cfg')
    #print(str(basedir))
    #app.config['SQLALCHEMY_DATABASE_URI'] = \
      #  'sqlite:///' + path.join(basedir, 'data.sqlite')
   # app.config['SQLAlCHEMY_COMMIT_ON_TEARDOWN'] = True
    db.init_app(app)
    bootstrap.init_app(app)
    nav.init_app(app)
    babel.init_app(app)
    login_manager.init_app(app)
    pagedowm.init_app(app)
    Gravatar(app,size=64)
    from auth import auth as auth_blueprint
    from main import main as main_blueprint
    app.register_blueprint(auth_blueprint,url_prefix='/auth')
    app.register_blueprint(main_blueprint,static_folder='static')

    @app.template_test('current_link')
    def is_current_link(link):
        return link == request.path

    @babel.localeselector
    def get_locale():
        return current_user.locale
    return app







#if __name__ == '__main__':
    #app.run(debug=True)
   # dev()
    # live_server=Server(app.wsgi_app)
    # live_server.watch('**/*.*')
    # live_server.serve(open_url=True)

