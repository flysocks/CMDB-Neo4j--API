import logging
import logging.handlers
import os

import markupsafe
import neomodel
from flask import Flask, jsonify
from flask_classful import route
from neomodel import (IntegerProperty, RelationshipFrom, RelationshipTo,
                      StringProperty, StructuredNode, StructuredRel,
                      UniqueIdProperty, EmailProperty)
from webargs import fields

from grest import GRest, models, utils
import global_config


class BranchInfo(StructuredRel, models.Relation):
    """Branch Information Model (for relationship)"""
    adopted_since = IntegerProperty()


class Branch(StructuredNode, models.Node):
    """Branch model"""
    branch_id = UniqueIdProperty()
    name = StringProperty()

    belong = RelationshipFrom("Host", "Belong_TO")
    manage = RelationshipFrom("Person", "Manage_TO")


class PersonInfo(StructuredRel, models.Relation):
    """Branch Information Model (for relationship)"""
    adopted_since = IntegerProperty()


class Person(StructuredNode, models.Node):
    """Branch model"""
    person_id = UniqueIdProperty()
    name = StringProperty()
    phone = StringProperty()
    email = StringProperty()

    manage_host = RelationshipFrom("Host", "Manage_TO")
    manage_software = RelationshipFrom("Software", "Manage_TO")
    manage_branch = RelationshipFrom("Branch", "Manage_TO")


class SoftwareInfo(StructuredRel, models.Relation):
    """Software Information Model (for relationship)"""
    adopted_since = IntegerProperty()


class Software(StructuredNode, models.Node):
    """Software model"""
    software_id = UniqueIdProperty()
    name = StringProperty()
    main_path = StringProperty()
    log_path = StringProperty()
    data_path = StringProperty()
    port = IntegerProperty()
    version = IntegerProperty()
    path_version = StringProperty()
    detail = StringProperty()

    perform = RelationshipTo("Host", "Perform_ON", model=SoftwareInfo)
    manage = RelationshipTo("Person", "Manage_TO", model=PersonInfo)


class Host(StructuredNode, models.Node):
    """Hosts model"""
    __validation_rules__ = {
        "name": fields.Str(),
        "ip": fields.Str(required=True),
        "cpu": fields.Str(),
        "mem": fields.Str(),
        "device": fields.Str()
    }

    __filtered_fields__ = ["secret_field"]

    host_id = UniqueIdProperty()
    name = StringProperty()
    ip = StringProperty()
    cpu = StringProperty()
    mem = StringProperty()
    device = StringProperty()
    secret_field = StringProperty(default="secret", required=False)

    branches = RelationshipTo(Branch, "Belong_TO", model=BranchInfo)
    softwares = RelationshipFrom(Software, "Perform_ON")
    persons = RelationshipFrom(Person, "Manage_TO")


class HostsView(GRest):
    """Hosts's View (/hosts)"""
    __model__ = {"primary": Host,
                 "secondary": {
                     "branches": Branch,
                     "softwares": Software,
                     "persons": Person
                 }}

    __selection_field__ = {"primary": "host_id",
                           "secondary": {
                               "branches": "branch_id",
                               "softwares": "software_id",
                               "persons": "person_id"
                           }}


class BranchesView(GRest):
    """Branch's View (/Branches)"""
    __model__ = {"primary": Branch}
    __selection_field__ = {"primary": "branch_id"}

    """主机所属分支"""
    @route("/<branch_id>/belong", methods=["GET"])
    def belong(self, branch_id):
        try:
            branch = Branch.nodes.get(**{self.__selection_field__.get("primary"): str(markupsafe.escape(branch_id))})

            if (branch):

                current_belong = branch.belong.get()

                if (current_belong):
                    return jsonify(owner=current_belong.to_dict()), 200
                else:
                    return jsonify(errors=["Selected Branch has not been adopted yet!"]), 404
            else:
                return jsonify(errors=["Selected Branch does not exists!"]), 404
        except:
            return jsonify(errors=["An error occurred while processing your request."]), 500

    """分支管理员"""
    @route("/<branch_id>/manage", methods=["GET"])
    def manage(self, branch_id):
        try:
            branch = Branch.nodes.get(**{self.__selection_field__.get("primary"): str(markupsafe.escape(branch_id))})

            if (branch):
                current_manage = branch.manage.get()
                if (current_manage):
                    return jsonify(owner=current_manage.to_dict()), 200
                else:
                    return jsonify(errors=["Selected Branch has not been adopted yet!"]), 404
            else:
                return jsonify(errors=["Selected Branch does not exists!"]), 404
        except:
            return jsonify(errors=["An error occurred while processing your request."]), 500


class SoftwaresView(GRest):
    """Branch's View (/Branches)"""
    __model__ = {"primary": Software}
    __selection_field__ = {"primary": "software_id"}

    """应用部署到那主机"""
    @route("/<software_id>/perform", methods=["GET"])
    def perform(self, software_id):
        try:
            software = Software.nodes.get(**{self.__selection_field__.get("primary"):
                                                 str(markupsafe.escape(software_id))})

            if (software):
                current_perform = software.perform.get()
                if (current_perform):
                    return jsonify(owner=current_perform.to_dict()), 200
                else:
                    return jsonify(errors=["Selected Software has not been adopted yet!"]), 404
            else:
                return jsonify(errors=["Selected Software does not exists!"]), 404
        except:
            return jsonify(errors=["An error occurred while processing your request."]), 500

    """应用开发者,运维者"""
    @route("/<software_id>/manage", methods=["GET"])
    def manage(self, software_id):
        try:
            software = Software.nodes.get(**{self.__selection_field__.get("primary"):
                                                 str(markupsafe.escape(software_id))})

            if (software):
                current_manage = software.manage.get()
                if (current_manage):
                    return jsonify(owner=current_manage.to_dict()), 200
                else:
                    return jsonify(errors=["Selected Software has not been adopted yet!"]), 404
            else:
                return jsonify(errors=["Selected Software does not exists!"]), 404
        except:
            return jsonify(errors=["An error occurred while processing your request."]), 500


class PersonsView(GRest):
    """Person's View (/Persons)"""
    __model__ = {"primary": Person}
    __selection_field__ = {"primary": "person_id"}

    """主机管理"""
    @route("/<person_id>/manage_host", methods=["GET"])
    def manage_host(self, software_id):
        try:
            person = Person.nodes.get(**{self.__selection_field__.get("primary"):
                                             str(markupsafe.escape(person_id))})

            if (person):
                current_manage_host = person.manage_host.get()
                if (current_manage_host):
                    return jsonify(owner=current_manage_host.to_dict()), 200
                else:
                    return jsonify(errors=["Selected Software has not been adopted yet!"]), 404
            else:
                return jsonify(errors=["Selected Software does not exists!"]), 404
        except:
            return jsonify(errors=["An error occurred while processing your request."]), 500

    """应用管理"""
    @route("/<person_id>/manage_software", methods=["GET"])
    def manage_software(self, software_id):
        try:
            person = Person.nodes.get(**{self.__selection_field__.get("primary"):
                                             str(markupsafe.escape(person_id))})

            if (person):
                current_manage_software = person.manage_software.get()
                if (current_manage_software):
                    return jsonify(owner=current_manage_software.to_dict()), 200
                else:
                    return jsonify(errors=["Selected Software has not been adopted yet!"]), 404
            else:
                return jsonify(errors=["Selected Software does not exists!"]), 404
        except:
            return jsonify(errors=["An error occurred while processing your request."]), 500

    """分支管理"""
    @route("/<person_id>/manage_branch", methods=["GET"])
    def manage_branch(self, software_id):
        try:
            person = Person.nodes.get(**{self.__selection_field__.get("primary"):
                                             str(markupsafe.escape(person_id))})

            if (person):
                current_manage_branch = person.manage_branch.get()
                if (current_manage_branch):
                    return jsonify(owner=current_manage_branch.to_dict()), 200
                else:
                    return jsonify(errors=["Selected Software has not been adopted yet!"]), 404
            else:
                return jsonify(errors=["Selected Software does not exists!"]), 404
        except:
            return jsonify(errors=["An error occurred while processing your request."]), 500


def cmdb_api():
    cmdb_api = Flask(__name__)

    @cmdb_api.route('/')
    def index():
        return "CMDB API V1"

    neomodel.config.DATABASE_URL = global_config.DB_URL
    neomodel.config.AUTO_INSTALL_LABELS = True
    neomodel.config.FORCE_TIMEZONE = True  # default False

    HostsView.register(cmdb_api, route_base="/hosts", trailing_slash=False)
    BranchesView.register(cmdb_api, route_base="/branches", trailing_slash=False)
    SoftwaresView.register(cmdb_api, route_base="/softwares", trailing_slash=False)
    PersonsView.register(cmdb_api, route_base="/persons", trailing_slash=False)

    return cmdb_api


if __name__ == '__main__':
    cmdb_api = cmdb_api()
    # app.run()
    cmdb_api.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
