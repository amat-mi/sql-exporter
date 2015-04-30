import sys
import json

class SQLExporter(object):
    
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = self.parse_config()



    def parse_config(self):
        with open(self.config_file) as fl:
            return json.load(fl)


    def get_ftp_config(self):
        return self.config["ftp"]


    def get_db_config(self):
        return self.config["db"]

    def get_queries(self):
        queries = self.config("queries")


    def run(self):
        pass




if __name__ == "__main__":
    xporter = SQLExporter("config.json")
    xporter.run()