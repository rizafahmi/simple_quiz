from pyramid.config import Configurator
from pyramid.mako_templating import renderer_factory as mako_factory
from pyramid.events import NewRequest

from urlparse import urlparse
import pymongo


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_renderer('.html', mako_factory)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('new', '/')
    config.add_route('quiz', '/user/{username}/account/{account_type}')
    config.add_route('posting', '/posting')
    config.add_route('notloggedin', '/notloggedin')
    config.add_route('loginerror', '/loginerror')
    config.add_route('saranghae100', '/saranghae100')

    # MongoDB Setting
    db_url = urlparse(settings['mongo_uri'])
    conn = pymongo.Connection(host=db_url.hostname, port=db_url.port)
    config.registry.settings['db_conn'] = conn

    def add_mongo_db(event):
        settings = event.request.registry.settings
        db = settings['db_conn'][db_url.path[1:]]
        if db_url.username and db_url.password:
            db.authenticate(db_url.username, db_url.password)

        event.request.db = db

    config.add_subscriber(add_mongo_db, NewRequest)

    config.scan()
    return config.make_wsgi_app()
