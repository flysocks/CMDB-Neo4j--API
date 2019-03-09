#coding=utf-8

import global_config
from cmdb_model import *
import markupsafe
import neomodel
import logging
from flask import Flask, jsonify
from flask_classful import route
from grest import GRest
from flask_cors import CORS

# from flask_restplus import Resource, Api
from flask_restful_swagger_2 import Api, swagger, Resource

# 通过下面的方式进行简单配置输出方式与日志级别
logging.basicConfig(filename='logger.log', level=logging.INFO)

logging.debug('debug message')
logging.info('info message')
logging.warn('warn message')
logging.error('error message')
logging.critical('critical message')


class AppView(GRest):
    """
    App view (/app)
    1. (App)-[USE]->(DevLanguage)
    2. (App)-[USE]->(ServiceType)
    3. (App)-[USE]->(ServletsEngine)
    4. (App)-[USE]->(ConfigType)

    5. (App)-[Belong_TO]->(Environment)
    6. (App)-[Depend_ON]->(Host)
    7. (App)-[USE]->(DatabaseConnect)
    8. (App)-[USE]->(FileServer)
    9. (App)-[Depend_ON]->(K8SNamespace)
    10. (person)-[Manager_TO]->(app)
    """

    __model__ = {
        "primary": App,
        "secondary": {
            "devlanguage": DevLanguage,
            "servicetype": ServiceType,
            "servletsengine": ServletsEngine,
            "configtype": ConfigType,
            "environment": Environment,
            "host": Host,
            "databaseconnect": DatabaseConnect,
            "fileserver": FileServer,
            "k8snamespace": K8SNamespace,
            "person": Person
        }
    }

    __selection_field__ = {
        "primary": "app_id",
        "secondary": {
            "devlanguage": "devlanguage_id",
            "servicetype": "servicetype_id",
            "servletsengine": "servletsengine_id",
            "configtype": "configtype_id",
            "environment": "environment_id",
            "host": "host_id",
            "databaseconnect": "databaseconnect_id",
            "fileserver": "fileserver_id",
            "k8snamespace": "k8snamespace_id",
            "person": "person_id"
        }

    }


class DevLanguageView(GRest):
    """
    dev language view (/devlanguage)
    1. (app)-[USE]->(DevLanguage)
    """
    __model__ = {
        "primary": DevLanguage,
        "secondary": {
            "app": App
        }
    }

    __selection_field__ = {
        "primary": "devlanguage_id",
        "secondary": {
            "app": "app_id"
        }
    }


class ServiceTypeView(GRest):
    """
    service type view (/servicetype)
    1. (app)-[USE]->(ServiceType)
    """
    __model__ = {
        "primary": ServiceType,
        "secondary": {
            "app": App
        }
    }

    __selection_field__ = {
        "primary": "servicetype_id",
        "secondary": {
            "app": "app_id"
        }
    }


class ServletsEngineView(GRest):
    """
    servlets engine  view (/servletsengine)
    1. (app)-[USE]->(ServletsEngine)
    """
    __model__ = {
        "primary": ServletsEngine,
        "secondary": {
            "app": App
        }
    }

    __selection_field__ = {
        "primary": "servletsengine_id",
        "secondary": {
            "app": "app_id"
        }
    }


class ConfigTypeView(GRest):
    """
    config type view (/configtype)
    1. (app)-[USE]->(ConfigType)
    """
    __model__ = {
        "primary": ConfigType,
        "secondary": {
            "app": App
        }
    }

    __selection_field__ = {
        "primary": "configtype_id",
        "secondary": {
            "app": "app_id"
        }
    }


class HostView(GRest):
    """
    Hosts View (/host)
    1. (host)-[Belong_TO]->(Environment)
    2. (app)-[Depend_ON]->(host)
    3. (DB)-[Depend_ON]->(host)
    4. (MD)-[Depend_ON]->(host)
    """
    __model__ = {
        "primary": Host,
        "secondary": {
            "environment": Environment,
            "recommendedtype": RecommendedType,
            "app": App,
            "db": DB,
            "md": MD
        }
    }

    __selection_field__ = {
        "primary": "host_id",
        "secondary": {
            "environment": "environment_id",
            "recommendedtype": "recommendedtype_id",
            "app": "app_id",
            "db": "db_id",
            "md": "md_id"
        }
    }


class EnvironmentView(GRest):
    """
    Environment View (/environment)
    1. (App)-[Belong_TO]->(Environment)
    2. (Host)-[Belong_TO]->(Environment)
    3. (DatabaseConnect)-[Belong_TO]->(Environment)
    4. (FileServer)-[Belong_TO]->(Environment)
    5. (K8SNamespace)-[Belong_TO]->(Environment)
    6. (DB)-[Belong_TO]->(Environment)
    7. (MD)-[Belong_TO]->(Environment)
    8. (Person)-[Manage_TO]->(Environment)
    """
    __model__ = {
        "primary": Environment,
        "secondary": {
            "app": App,
            "host": Host,
            "databaseconnect": DatabaseConnect,
            "fileserver": FileServer,
            "k8snamespace": K8SNamespace,
            "db": DB,
            "md": MD,
            "person": Person
        }
    }

    __selection_field__ = {
        "primary": "environment_id",
        "secondary": {
            "app": "app_id",
            "host": "host_id",
            "databaseconnect": "databaseconnect_id",
            "fileserver": "fileserver_id",
            "k8snamespace": "k8snamespace_id",
            "db": "db_id",
            "md": "md_id",
            "person": "person_id"
        }
    }


class FileServerView(GRest):
    """
    FileServer View (/fileServer)
    1. (App)-[USE]->(FileServer)
    2. (FileServer)-[Belong_TO]->(Environment)
    """
    __model__ = {
        "primary": FileServer,
        "secondary": {
            "environment": Environment,
            "app": App
        }
    }

    __selection_field__ = {
        "primary": "fileserver_id",
        "secondary": {
            "environment": "environment_id",
            "app": "app_id"
        }

    }


class DatabaseConnectView(GRest):
    """
    DatabaseConnect View (/databaseconnect)
    1. (App)-[USE]->(DatabaseConnect)
    2. (DatabaseConnect)-[Belong_TO]->(Environment)
    3. (DatabaseConnect)-[Belong_TO]->(DB)
    """
    __model__ = {
        "primary": DatabaseConnect,
        "secondary": {
            "app": App,
            "environment": Environment,
            "db": DB
        }
    }

    __selection_field__ = {
        "primary": "dbconnect_id",
        "secondary": {
            "app:": "app_id",
            "environment": "environment_id",
            "db": "db_id"
        }
    }


class DBView(GRest):
    """
    DBView View (/db)"
    1. (DatabaseConnect)-[Belong_TO]->(DB)
    2. (DB)-[Belong_TO]->(Environment)
    3. (DB)-[Depend_ON]->(Host)
    """
    __model__ = {
        "primary": DB,
        "secondary": {
            "host": Host,
            "environment": Environment,
            "databaseconnect": DatabaseConnect
        }
    }

    __selection_field__ = {
        "primary": "db_id",
        "secondary": {
            "host": "host_id",
            "environment": "environment_id",
            "databaseconnect": "databaseconnect_id"
        }
    }


class K8SNamespaceView(GRest):
    """
    K8SNamespace View (/k8snamespace)
    1. (K8SNamespace)-[Belong_TO]->(Environment)
    2. (K8SNamespace)-[Belong_TO]->(K8S)
    3. (App)-[Depend_ON]->(K8SNamespace)
    """
    __model__ = {
        "primary": K8SNamespace,
        "secondary": {
            "environment": Environment,
            "k8s": K8S,
            "app": App
        }
    }

    __selection_field__ = {
        "primary": "k8sns_id",
        "secondary": {
            "environment": "environment_id",
            "k8s": "k8s_id",
            "app": "app_id"
        }
    }


class PersonView(GRest):
    """
    Person View (/person)
    1. (person)-[Manage_TO]->(Environment)
    2. (person)-[Manage_TO]->(App)
    """

    __model__ = {
        "primary": Person,
        "secondary": {
            "environment": Environment,
            "app": App
        }
    }

    __selection_field__ = {
        "primary": "person_id",
        "secondary": {
            "environment": "environment_id",
            "app": "app_id"
        }
    }


def cmdb_api():
    app = Flask(__name__, static_folder='apidocs/apidocs/static')
    CORS(app)
    # Api(app)

    # logging.getLogger('flask_cors').level = logging.DEBUG

    @app.route('/')
    def index():
        return app.send_static_file('index.html')


    neomodel.config.DATABASE_URL = global_config.DB_URL
    neomodel.config.AUTO_INSTALL_LABELS = True
    neomodel.config.FORCE_TIMEZONE = True  # default False

    AppView.register(app, route_base="/app", trailing_slash=False, route_prefix="/v1")
    HostView.register(app, route_base="/host", trailing_slash=False, route_prefix="/v1")
    EnvironmentView.register(app, route_base="/environment", trailing_slash=False, route_prefix="/v1")
    FileServerView.register(app, route_base="/fileserver", trailing_slash=False, route_prefix="/v1")
    DatabaseConnectView.register(app, route_base="/databaseconnect", trailing_slash=False, route_prefix="/v1")
    DBView.register(app, route_base="/db", trailing_slash=False, route_prefix="/v1")
    K8SNamespaceView.register(app, route_base="/k8snamespace", trailing_slash=False, route_prefix="/v1")
    PersonView.register(app, route_base="/person", trailing_slash=False, route_prefix="/v1")

    # app 使用到的在"开发语言""服务框架""web引擎""配置类型"
    DevLanguageView.register(app, route_base="/devlanguage", trailing_slash=False, route_prefix="/v1")
    ServiceTypeView.register(app, route_base="/servicetype", trailing_slash=False, route_prefix="/v1")
    ServletsEngineView.register(app, route_base="/servletsengine", trailing_slash=False, route_prefix="/v1")
    ConfigTypeView.register(app, route_base="/configtype", trailing_slash=False, route_prefix="/v1")

    return app


if __name__ == '__main__':
    app = cmdb_api()
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
