import os
import sys 
CURRENT_DIR = os.path.split(os.path.abspath(__file__))[0]  # 当前目录
config_path = CURRENT_DIR.rsplit('/', 1)[0]  # 上三级目录
sys.path.append(config_path)

import sqlite3
import json

from sqlite_db import  SqliteDB
from config import DB_DIR
from entity.stryd_activity import StrydActivity



class StrydDB:
    
    def __init__(self, stryd_db_name):
        ## Stryd数据库
        self._stryd_db_name = stryd_db_name
    
    @property
    def stryd_db_name(self):
        return self._stryd_db_name
    
    ## 保存Stryd运动信息
    def saveActivity(self, stryd_activity):
        activity_id = stryd_activity.activity_id
        activity_data = stryd_activity.activity_data
        exists_select_sql = 'SELECT * FROM stryd_activity WHERE activity_id = ?'
        with SqliteDB(self._stryd_db_name) as db:
            exists_query_set = db.execute(exists_select_sql, (activity_id,)).fetchall()
            query_size = len(exists_query_set)
            if query_size == 0:
              db.execute('insert into stryd_activity (activity_id, activity_data) values (?, ?)', (activity_id, json.dumps(activity_data)) )
    
    def getUnSyncActivity(self):
        select_un_upload_sql = 'SELECT activity_id FROM stryd_activity WHERE is_sync_connect = 0'
        with SqliteDB(self._stryd_db_name) as db:
            un_upload_result = db.execute(select_un_upload_sql).fetchall()
            query_size = len(un_upload_result)
            if query_size == 0:
                return None
            else:
                activity_id_list = []
                for result in un_upload_result:
                    activity_id_list.append(result[0])
                return activity_id_list
    
    def updateSyncStatus(self, activity_id:int):
        update_sql = "update stryd_activity set is_sync_connect = 1 WHERE activity_id = ?"
        with SqliteDB(self._stryd_db_name) as db:
          db.execute(update_sql, (activity_id,))

    def initDB(self):
      with SqliteDB(os.path.join(DB_DIR, self._stryd_db_name)) as db:
          db.execute('''
          
          CREATE TABLE stryd_activity(
              id INTEGER NOT NULL PRIMARY KEY  AUTOINCREMENT ,
              activity_id INTEGER NOT NULL  , 
              activity_data TEXT ,
              is_sync_connect INTEGER NOT NULL  DEFAULT 0,
              create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
              update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
          ) 

          '''
          )
