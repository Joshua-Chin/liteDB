import pickle
import sqlite3

class connect(object):

    def __init__(self, database):
        self.database = database
        with sqlite3.connect(database) as c:
            cmd = "select * from sqlite_master where type='table'"
            if not [table for table in c.execute(cmd)
                    if table[1]=='liteDB']:
                c.execute("create table liteDB(data blob)")
                
    def add(self, item):
        item = pickle.dumps(item)
        with sqlite3.connect(self.database) as c:
            cmd = "insert into liteDB values (:item)"
            c.execute(cmd,{'item':item})

    def discard(self, item):
        item = pickle.dumps(item)
        with sqlite3.connect(self.database) as c:
            cmd = "delete from liteDB where data=:item"
            c.execute(cmd,{'item':item})

    def __iter__(self):
        with sqlite3.connect(self.database) as c:
            cmd = "select * from liteDB"
            return map(lambda x:pickle.loads(x[0]),
                       list(c.execute(cmd)))

    def __len__(self):
        with sqlite3.connect(self.database) as c:
            cmd = "select count(*) from liteDB"
            return next(c.execute(cmd))[0]

