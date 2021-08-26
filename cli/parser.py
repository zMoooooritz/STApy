#!/usr/bin/env python

import argparse

from common.log import Log
from common.config import config, set_api_url
from cli.cli import request

class Parser(object):

    args = None

    def __init__(self):
        self.construct_parser()

    def construct_parser(self):
        parser = argparse.ArgumentParser(
            description="Access and modify data that is stored in a server that uses the SensorThings API (v1.1+)",
            prog="STApy", epilog="")
        parser.add_argument("-l", "--log", type=Log.from_string, choices=list(Log), default=Log.INFO,
                            help="define the log level", metavar="CRITICAL,ERROR,WARNING,INFO,DEBUG,NOTSET")
        parser.add_argument("-u", "--url-set", dest="urlset", nargs=1, metavar=("URL"),
                            help="set the url of the SensorThings API backend")
        parser.add_argument("-ug", "--url-get", dest="urlget", action="store_true",
                            help="get the url of the SensorThings API backend")
        parser.add_argument("-a", "--add", nargs="+", metavar=("Entity", "Parameters"),
                            help="add new entities")
        parser.add_argument("-d", "--del", nargs="+", dest="delete", metavar=("Entity", "ID"),
                            help="delete entities by id or path")
        parser.add_argument("-g", "--get", nargs="+", dest="getr", metavar=("Entity", "ID/Path"),
                            help="get the content of entities by id or path")
        parser.add_argument("-i", "--inter", action="store_true",
                            help="start the interactive CLI mode for requests")

        self.args = parser.parse_args()

    def get_log_level(self):
        return self.args.log.value

    def parse_args(self):
        if self.args.urlset:
            set_api_url(self.args.urlset)
        if self.args.urlget:
            print("The currently set API_URL is: " + str(config.get("API_URL")))

        if (self.args.add or self.args.delete or self.args.getr) and config.get("API_URL") == "":
            logger.critical("The url has to be set before using the application (see --help)")
            logger.info("ending application")
            return True

        if self.args.add:
            func = Post.get_entity_method(Entity.match(self.args.add[0]))
            if func == None:
                logger.error("The supplied entity (" + self.args.add[0] + ") is not valid")
                logger.error("The valid entities are: " + ", ".join(Entity.list()))
            else:
                req_args = []
                for param in signature(func).parameters.values():
                    if param.default is param.empty:
                        req_args.append(param.name)

                if len(req_args) > len(args.add)-1:
                    logger.error("Not enough arguments supplied for the entity " + Entity.get(self.args.add[0]).value)
                    logger.error("The following arguments are mandatory (in this order): " + ", ".join(req_args))
                else:
                    Post.new_entity(Entity.match(self.args.add[0]), *self.args.add[1:])

        if self.args.delete:
            entity = Entity.get(self.args.delete[0])
            if entity == None:
                logger.error("The supplied entity (" + self.args.delete[0] + ") is not valid")
                logger.error("The valid entities are: " + ", ".join(Entity.list()))
            else:
                for e_id in self.args.delete[1:]:
                    if e_id.isdigit():
                        requests.delete(Query(entity.value).entity_id(int(e_id)).get_query())
                    else:
                        logger.warning(str(e_id) + " is not a valid " + entity.value + "-ID")

        if self.args.getr:
            # path = Query(Entity.Locations.value).get_query()
            # print(JSONExtract(path).select("name").get_data_sets())
            pass

        if self.args.inter:
            request()