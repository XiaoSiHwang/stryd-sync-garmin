import urllib3
import json
from entity.login_user import LoginUser


class StrydClient:
    def __init__(self, login_user) -> None:
        
        self.email = login_user.email
        self.password = login_user.password
        self.req = urllib3.PoolManager()
        self.token = None
        self.id = None
    
    ## 登录接口
    def login(self):
        
        login_url = "https://api.stryd.com/b/email/signin"

        login_data = {
            "email": self.email,
            "password": self.password,
        }
        headers = {
          "Accept":       "application/json",
          "Content-Type": "application/json",
          "User-Agent":   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.39 Safari/537.36",
          "Referer": "https://www.stryd.com/signin",
        }

        login_body = json.dumps(login_data)
        response = self.req.request('POST', login_url, body=login_body, headers=headers)

        login_status_code = response.status
        login_response = json.loads(response.data)
        if login_status_code != 200:
            raise StrydLoginError("Stryd登录异常，异常原因为：" + login_response["message"])

        token = login_response["token"]
        id = login_response["id"]
        self.token = token
        self.id = id
    
    ## 获取所有Stryd运动信息
    def activities(self, include_deleted=False):

        ## 判断Token 是否为空
        if self.token == None:
            self.login()

        activities_url = f"https://api.stryd.com/b/api/v1/users/{self.id}/calendar?include_deleted={include_deleted}"

        headers = {
                  "Accept":       "application/json",
                  "Content-Type": "application/json",
                  "User-Agent":   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.39 Safari/537.36",
                  "authorization": f"Bearer: {self.token}",
                }        
        response = self.req.request('GET', activities_url, headers=headers)
        get_activities_status_code = response.status
        if get_activities_status_code != 200:
            raise StrydGetActivityError("Stryd获取活动信息异常" )
        activities_data = json.loads(response.data)
        return activities_data
    
    ## 获取Lgin
    def get_download_url(self, activity_id):
        
        ## 判断Token 是否为空
        if self.token == None:
            self.login()

        headers = {
                  "Accept":       "application/json",
                  "Content-Type": "application/json",
                  "origin": "https://www.stryd.com",
                  "referer": "https://www.stryd.com/",
                  "User-Agent":   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.39 Safari/537.36",
                  "authorization": f"Bearer: {self.token}",
                }       
        get_download_url = f"https://api.stryd.com/b/api/v1/users/{self.id}/activities/{activity_id}/fit"
        response = self.req.request('GET', get_download_url, headers=headers)
        get_download_status_code = response.status
        if get_download_status_code != 200:
            raise StrydGetActivityDownloadUrlError("Stryd获取下载活动链接异常！！" )
        response_data = json.loads(response.data)
        return response_data["url"]
    

class StrydLoginError(Exception):

    def __init__(self, status):
        """Initialize."""
        super(StrydLoginError, self).__init__(status)
        self.status = status

class StrydGetActivityError(Exception):

    def __init__(self, status):
        """Initialize."""
        super(StrydGetActivityError, self).__init__(status)
        self.status = status

class StrydGetActivityDownloadUrlError(Exception):

    def __init__(self, status):
        """Initialize."""
        super(StrydGetActivityError, self).__init__(status)
        self.status = status

