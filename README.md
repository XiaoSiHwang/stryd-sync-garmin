# Stryd 同步佳明脚本（支持国际区与国区）
## 致谢
- 本脚本佳明模块代码来自@[yihong0618](https://github.com/yihong0618) 的 [running_page](https://github.com/yihong0618/running_page) 个人跑步主页项目,在此非常感谢@[yihong0618](https://github.com/yihong0618)大佬的无私奉献！！！
## 注意
### 目前脚本不支持Stryd OAuth2的帐号即 Google、Facebook、Apple等帐号关联登录只支持邮箱密码登录

## 参数配置
|       参数名       |                备注                |    案例     |
| :----------------: | :--------------------------------: | :---------: |
|    GARMIN_EMAIL    |          佳明登录帐号邮箱          |             |
|  GARMIN_PASSWORD   |            佳明登录密码            |             |
| GARMIN_AUTH_DOMAIN | 佳明区域（国际区填:COM 国区填:CN） | (COM or CN) |
|    STRYD_EMAIL     |           Stryd 登录邮箱           |             |
|   STRYD_PASSWORD   |             Stryd 密码             |             |

## Github配置步骤
### 1.参数配置
打开**Setting**
![打开Setting](doc/3451692931372_.pic.jpg)
找到**Secrets and variables**点击**New repository secret**按钮
![Secrets and variables](/doc/3461692931472_.pic.jpg)
打开**New repository secret**后将上述的参数填入，下图以佳明帐号为例,**Name**填写参数名,**Secret**填写你的信息，重复以上步骤填入五个参数即可
![填入参数](doc/3471692931624_.pic.jpg)

### 2.配置WorkFlow权限
打开**Setting**找到**Actions**点击**General**按钮,按照下图勾选并save
![配置WorkFlow权限](doc/3481692931856_.pic.jpg)

### 3. wrokflow配置
打开**github/workflows/stryd-sync-garmin.yml**文件,将**GITHUB_NAME**更改为你的Github用户名、**GITHUB_EMAIL**更改为你的Github登录邮箱，更改步骤如下:
![更改步骤](doc/3491692932110_.pic.jpg)
更改完成后点击右上角**Commit changes...**提交即可
![Commit](doc/3501692932345_.pic.jpg)
