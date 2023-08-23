import os


import sys 
CURRENT_DIR = os.path.split(os.path.abspath(__file__))[0]  # 当前目录
config_path = CURRENT_DIR.rsplit('/', 1)[0]  # 上三级目录
sys.path.append(config_path)

import asyncio
import urllib3


from config import DB_DIR, STRYD_FIT_DIR
from stryd_db import StrydDB
from stryd_client import StrydClient
from stryd.entity.login_user import LoginUser
from stryd.entity.stryd_activity import StrydActivity
from garmin.garmin_connect import GarminConnect


SYNC_CONFIG = {
    'GARMIN_AUTH_DOMAIN': '',
    'GARMIN_EMAIL': '',
    'GARMIN_PASSWORD': '',
    "STRYD_EMAIL": '',
    "STRYD_PASSWORD": '',
}


def init(stryd_db):
    ## 判断RQ数据库是否存在
    print(os.path.join(DB_DIR, stryd_db.stryd_db_name))
    if not os.path.exists(os.path.join(DB_DIR, stryd_db.stryd_db_name)):
        ## 初始化建表
        stryd_db.initDB()
    if not os.path.exists(STRYD_FIT_DIR):
        os.mkdir(STRYD_FIT_DIR)


if __name__ == "__main__":

   # 首先读取 面板变量 或者 github action 运行变量
  for k in SYNC_CONFIG:
      if os.getenv(k):
          v = os.getenv(k)
          SYNC_CONFIG[k] = v

  ## db 名称
  db_name = "stryd.db"
  ## 建立DB链接
  stryd_db = StrydDB(db_name)
  ## 初始化DB位置和下载文件位置
  init(stryd_db)

  STRYD_EMAIL = SYNC_CONFIG["STRYD_EMAIL"]
  STRYD_PASSWORD = SYNC_CONFIG["STRYD_PASSWORD"]
  login_user = LoginUser(STRYD_EMAIL, STRYD_PASSWORD)
  strydClient = StrydClient(login_user)
  activities = strydClient.activities()

  for activity in activities["activities"]:
    s = StrydActivity()
    id = activity["id"]

    s.activity_id = id
    s.activity_data = activity
    stryd_db.saveActivity(s)

  ## 查询未上传的运动
  activity_id_list = stryd_db.getUnSyncActivity()

  ## 判断是否存在还未上传的运动
  if activity_id_list == None or len(activity_id_list) == 0:
      exit()

  req = urllib3.PoolManager()

  ## 建立主Garmin 链接
  GARMIN_EMAIL = SYNC_CONFIG["GARMIN_EMAIL"]
  GARMIN_PASSWORD = SYNC_CONFIG["GARMIN_PASSWORD"]
  GARMIN_AUTH_DOMAIN = SYNC_CONFIG["GARMIN_AUTH_DOMAIN"]
  garminConnect = GarminConnect(GARMIN_EMAIL,GARMIN_PASSWORD,GARMIN_AUTH_DOMAIN,False)

  loop = asyncio.get_event_loop()



  for activity_id in activity_id_list:
      download_url = strydClient.get_download_url(activity_id)
      file_path = os.path.join(STRYD_FIT_DIR, f"{activity_id}.fit")
      response = req.request('GET', download_url)
      with open(file_path, 'wb') as f:
        f.write(response.data)
      upload_activity_task = asyncio.ensure_future(garminConnect.upload_activities(file_path))
      upload_status = loop.run_until_complete(upload_activity_task)
      if upload_status in ("SUCCESS", "DUPLICATE_ACTIVITY"):
          stryd_db.updateSyncStatus(activity_id)
  loop.close()
        
