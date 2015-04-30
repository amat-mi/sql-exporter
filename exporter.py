import sys
import json
import ftplib
import datetime
import re
import os
import StringIO
import traceback

class SQLExporter(object):
    
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = self.parse_config()



    def parse_config(self):
        with open(self.config_file) as fl:
            return json.load(fl)
            

    def get_ftp_config(self):
        return self.config.get("ftp", None)


    def get_db_config(self):
        return self.config["db"]


    def get_queries(self):
        out = []
        queries = self.config["queries"]
        for query in queries:
            q = {}
            if "sql" in query:
                q["sql"] = query["sql"]
            elif "sql-file" in query:
                with open(query["sql-file"]) as qfl:
                    q["sql"] = qfl.read()

            if "csv" in query:
                q["csv"] = query["csv"]
            out.append(q)
        return out


    def get_connection(self):
        cfg = self.get_db_config()
        if cfg["type"] == "mssql":
            import pymssql
            return pymssql.connect(cfg["host"], cfg["user"], cfg["password"], cfg["database"])

        elif cfg["type"] == "sqlite":
            import sqlite3
            return sqlite3.connect(cfg["database"])

        # ...
        # elif  cfg["type"] == "postgres":
        # ...


        raise ValueError("Unknown db type")
        


    def csv_from_cursor(self, csv, cursor):
        """
        Writes csv file from open cursor
        returns file path
        """
        now = datetime.datetime.now()
        ex = re.compile("(?<=\[)(.*?)(?=\])")
        pieces = ex.findall(csv)
        for p in pieces:
            csv = csv.replace('['+p+']', datetime.datetime.strftime(now, p))

        with open(csv, "wb") as fl:
            for row in cursor:
                fl.write(",".join([str(x) for x in row]) + "\n")


        return csv

    def write_to_ftp(self, files):
        cfg = self.get_ftp_config()
        if not cfg or "host" not in cfg:
            return

        ftp = ftplib.FTP(cfg["host"])
        if "user" in cfg:
            ftp.login(cfg["user"], cfg["password"])
        else:
            ftp.connect()

        if "cwd" in cfg:
            ftp.cwd(cfg["cwd"])

        for f in files:
            with open(f) as fl:             
                fname = os.path.basename(f)
                ftp.storbinary('STOR '+fname, fl)

        ftp.quit()



    def write_errors_to_ftp(self, errors):
        
        print "writing errors to ftp"
        cfg = self.get_ftp_config()
        
        now = datetime.datetime.now()

        ftp = ftplib.FTP(cfg["host"])
        if "user" in cfg:
            ftp.login(cfg["user"], cfg["password"])
        else:
            ftp.connect()

        if "cwd" in cfg:
            ftp.cwd(cfg["cwd"])

        o = StringIO.StringIO()
        for err in errors:
            o.write(str(err) + "\n")   
        
        o.seek(0)

        errors_template = "errors_%Y_%m_%d__%H_%M_%S.txt"
        fname = datetime.datetime.strftime(now, errors_template)
        ftp.storbinary('STOR '+fname, o)

        ftp.quit()




    def run(self):
        queries = self.get_queries()
        csv_done = []
        errors = []

        with self.get_connection() as conn:
            for query in queries:
                cursor = conn.cursor()

                try:
                    cursor.execute(query["sql"])
                
                    if "csv" in query:
                        c = self.csv_from_cursor(query["csv"], cursor)
                        csv_done.append(c)
                    cursor.close()
                except Exception, e:
                    #print e
                    #raise e
                    s = traceback.format_exc()
                    errors.append(s)

        if  len(errors):
            self.write_errors_to_ftp(errors)
            return 1
        
        
        self.write_to_ftp(csv_done)
        return 0





if __name__ == "__main__":
    xporter = SQLExporter("config.json")
    xporter.run()