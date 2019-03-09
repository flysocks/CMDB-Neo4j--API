from global_config import *
from neomodel import (IntegerProperty, RelationshipFrom, RelationshipTo,
                      StringProperty, StructuredNode, StructuredRel,
                      UniqueIdProperty, EmailProperty, BooleanProperty, FloatProperty)
from grest import models


class EnvironmentInfo(StructuredRel, models.Relation):
    """ environment information model (for relationship) """
    adopted_since = IntegerProperty()


class Environment(StructuredNode, models.Node):
    """
    environment model
    1. (App)-[Belong_TO]->(Environment)
    2. (Host)-[Belong_TO]->(Environment)
    3. (DatabaseConnect)-[Belong_TO]->(Environment)
    4. (FileServer)-[Belong_TO]->(Environment)
    5. (K8SNamespace)-[Belong_TO]->(Environment)
    6. (DB)-[Belong_TO]->(Environment)
    7. (MD)-[Belong_TO]->(Environment)
    8. (Person)-[Manage_TO]->(Environment)
    """
    environment_id = UniqueIdProperty()
    environment_name = StringProperty()
    environment_status = StringProperty()

    app_belong = RelationshipFrom("App", "Belong_TO")
    host_belong = RelationshipFrom("Host", "Belong_TO")
    fileserver_belong = RelationshipFrom("FileServer", "Belong_TO")
    databaseconnect_belong = RelationshipFrom("DatabaseConnect", "Belong_TO")
    k8snamespace_belong = RelationshipFrom("K8SNamespace", "Belong_TO")
    db_belong = RelationshipFrom("DB", "Belong_TO")
    md_belong = RelationshipFrom("MD", "Belong_TO")
    person_manage = RelationshipFrom("Person", "Manage_TO")


class RecommendedTypeInfo(StructuredRel, models.Relation):
    """ hosts  recommended type  (for relationship) """
    adopted_since = IntegerProperty()
    
    
class RecommendedType(StructuredNode, models.Node):
    """
    host recommended type model
    1. (host)-[USE]->(recommendedType)
    """
    recommendedtype_id = UniqueIdProperty()
    recommendedtype_name = StringProperty()
    
    host_use = RelationshipFrom("Host", "USE")
    

class HostInfo(StructuredRel, models.Relation):
    """ Host information model (for relationship) """
    adopted_since = IntegerProperty()


class Host(StructuredNode, models.Node):
    """
    host model
    1. (host)-[Belong_TO]->(Environment)
    2. (app)-[Depend_ON]->(host)
    3. (DB)-[Depend_ON]->(host)
    4. (MD)-[Depend_ON]->(host)
    """
    host_id = UniqueIdProperty()
    host_name = StringProperty()
    private_ip = StringProperty()
    public_ip = StringProperty()
    CPU = StringProperty()
    memory = StringProperty()
    OS = StringProperty()
    OS_drive = StringProperty()
    data_drive = StringProperty()
    # recommended_type = StringProperty()

    environment = RelationshipTo(Environment, "Belong_TO", model=EnvironmentInfo)
    recommendedtype = RelationshipTo(RecommendedType, "USE", model=RecommendedTypeInfo)
    
    app_depend = RelationshipFrom("App", "Depend_ON")
    
    db_depend = RelationshipFrom("DB", "Depend_ON")
    md_depend = RelationshipFrom("MD", "Depend_ON")


class FileServerInfo(StructuredRel, models.Relation):
    """ file server information model (for relationship) """
    adopted_since = IntegerProperty()


class FileServer(StructuredNode, models.Node):
    """
    file server model
    1. (App)-[USE]->(FileServer)
    2. (FileServer)-[Belong_TO]->(Environment)
    """
    fileserver_id = UniqueIdProperty()
    fileserver_type = StringProperty()
    fileserver_name = StringProperty()
    fileserver_domain = StringProperty()
    fileserver_detail = StringProperty()

    app_use = RelationshipFrom("App", "USE")
    environment = RelationshipTo(Environment, "Belong_TO", model=EnvironmentInfo)


class DBInfo(StructuredRel, models.Relation):
    """ db information model (for relationship ) """
    adopted_since = IntegerProperty()


class DB(StructuredNode, models.Node):
    """
    db model
    1. (DatabaseConnect)-[Belong_TO]->(DB)
    2. (DB)-[Belong_TO]->(Environment)
    3. (DB)-[Depend_ON]->(Host)
    """
    db_id = UniqueIdProperty()
    db_name = StringProperty()
    db_main_path = StringProperty()
    db_data_path = StringProperty()
    db_los_path = StringProperty()
    db_version = StringProperty()

    databaseconnect_belong = RelationshipFrom("DatabaseConnect", "Belong_TO")
    environment = RelationshipTo(Environment, "Belong_TO", model=EnvironmentInfo)
    host = RelationshipTo(Host, "Depend_ON", model=HostInfo)


class DatabaseConnectInfo(StructuredRel, models.Relation):
    """ DatabaseConnect information model (for relationship) """
    adopted_since = IntegerProperty()


class DatabaseConnect(StructuredNode, models.Node):
    """
    DatabaseConnect model
    1. (App)-[USE]->(DatabaseConnect)
    2. (DatabaseConnect)-[Belong_TO]->(Environment)
    3. (DatabaseConnect)-[Belong_TO]->(DB)
    """
    databaseconnect_id = UniqueIdProperty()
    databaseconnect_type = StringProperty()
    databaseconnect_name = StringProperty()
    databaseconnect_username = StringProperty()
    databaseconnect_connect_key = StringProperty()

    app_use = RelationshipFrom("App", "USE")
    environment = RelationshipTo(Environment, "Belong_TO", model=EnvironmentInfo)
    db = RelationshipTo(DB, "Belong_TO", model=DBInfo)


class MDInfo(StructuredRel, models.Relation):
    """ md information model (for relationship) """
    adopted_since = IntegerProperty()


class MD(StructuredNode, models.Node):
    """
    md model
    1. MD)-[Belong_TO]->(Environment)
    2. (MD)-[Depend_ON]->(Host)
    """
    md_id = UniqueIdProperty()
    md_name = StringProperty()
    md_main_path = StringProperty()
    md_data_path = StringProperty()
    md_los_path = StringProperty()
    md_version = StringProperty()

    environment = RelationshipTo(Environment, "Belong_TO", model=EnvironmentInfo)
    host_depend = RelationshipFrom("Host", "Depend_ON")


class K8SInfo(StructuredRel, models.Relation):
    """ k8s information model (for relationship)"""
    adopted_since = IntegerProperty()


class K8S(StructuredNode, models.Node):
    """
    k8s model
    1. (K8SNamespace)-[Belong_TO]->(K8S)
    """
    k8s_id = UniqueIdProperty()
    k8s_name = StringProperty()

    k8snamespace_belong = RelationshipFrom("K8SNamespace", "Belong_TO")


class K8SNamespaceInfo(StructuredRel, models.Relation):
    """ k8s namespace information model (for relationship) """
    adopted_since = IntegerProperty()


class K8SNamespace(StructuredNode, models.Node):
    """
    k8s namespace model
    1. (K8SNamespace)-[Belong_TO]->(Environment)
    2. (K8SNamespace)-[Belong_TO]->(K8S)
    3. (App)-[Depend_ON]->(K8SNamespace)
    """
    k8snamespace_id = UniqueIdProperty()
    k8snamespace_name = StringProperty()

    environment = RelationshipTo(Environment, "Belong_TO", model=EnvironmentInfo)
    k8s = RelationshipTo(K8S, "Belong_TO", model=K8SInfo)
    app_depend = RelationshipFrom("App", "Depend_ON")


class DevLanguageInfo(StructuredRel, models.Relation):
    """ dev language information model (for relationship) """
    adopted_since = IntegerProperty()


class DevLanguage(StructuredNode, models.Node):
    """
    dev language model
    (app)-[USE]->(DevLanguage)
    """
    devlanguage_id = UniqueIdProperty()
    devlanguage_name = StringProperty()

    app_use = RelationshipFrom("App", "USE")


class ServiceTypeInfo(StructuredRel, models.Relation):
    """ service type information model (for relationship) """
    adopted_since = IntegerProperty()


class ServiceType(StructuredNode, models.Node):
    """
    service type model
    1. (app)->[USE]->(servicetype)
    """
    servicetype_id = UniqueIdProperty()
    servicetype_name = StringProperty()

    app_use = RelationshipFrom("App", "USE")


class ServletsEngineInfo(StructuredRel, models.Relation):
    """ servlets engine information model (for relationship) """
    adopted_since = IntegerProperty()


class ServletsEngine(StructuredNode, models.Node):
    """
    servlets engine model
    1. (app)->[USE]->(ServletsEngine)
    """
    servletsengine_id = UniqueIdProperty()
    servletsengine_name = StringProperty()

    app_use = RelationshipFrom("App", "USE")


class ConfigTypeInfo(StructuredRel, models.Relation):
    """ config type information model (for relationship) """
    adopted_since = IntegerProperty()


class ConfigType(StructuredNode, models.Node):
    """ config type model """
    configtype_id = UniqueIdProperty()
    configtype_name = StringProperty()

    app_use = RelationshipFrom("App", "USE")


class AppInfo(StructuredRel, models.Relation):
    """ Software Information Model (for relationship) """
    adopted_since = IntegerProperty()


class App(StructuredNode, models.Node):
    """
    app model
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
    app_id = UniqueIdProperty()
    app_name = StringProperty()
    code_git_path = StringProperty()
    CD_path = StringProperty()
    port = IntegerProperty()
    smoke_test = BooleanProperty()
    code_review = BooleanProperty()
    config_type = StringProperty()
    config_namespace = StringProperty()
    version = FloatProperty()
    run_status = StringProperty()

    # app使用开发语言,服务类型, web服务框架, 配置类型
    devlanguage = RelationshipTo(DevLanguage, "USE", model=DevLanguageInfo)
    servicetype = RelationshipTo(ServiceType, "USE", model=ServiceTypeInfo)
    servletsengine = RelationshipTo(ServletsEngine, "USE", model=ServletsEngineInfo)
    configtype = RelationshipTo(ConfigType, "USE", model=ConfigTypeInfo)

    environment = RelationshipTo(Environment, "Belong_TO", model=EnvironmentInfo)
    host = RelationshipTo(Host, 'Depend_ON', model=HostInfo)
    databaseconnect = RelationshipTo(DatabaseConnect, "USE", model=DatabaseConnectInfo)
    fileServer = RelationshipTo(FileServer, "USE", model=FileServerInfo)
    k8snamespace = RelationshipTo(K8SNamespace, "Depend_ON", model=K8SNamespaceInfo)
    person = RelationshipFrom('Person', "Manage_TO")


class PersonInfo(StructuredRel, models.Relation):
    """ person Information Model (for relationship) """
    adopted_since = IntegerProperty()


class Person(StructuredNode, models.Node):
    """
    person model
    1. (person)-[Manage_TO]->(Environment)
    2. (person)-[Manage_TO]->(App)
    """
    person_id = UniqueIdProperty()
    person_name = StringProperty()
    phone = StringProperty()
    email = EmailProperty()
    role = StringProperty()

    environment = RelationshipTo(Environment, "Manage_TO", model=EnvironmentInfo)
    app = RelationshipTo(App, "Manage_TO", model=AppInfo)


