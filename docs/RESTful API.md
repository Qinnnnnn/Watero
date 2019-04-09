### 1.Agent注册接口

#### 请求说明

> 请求方式 : GET<br>
请求URL : [http://47.101.186.138:5000/api/v1/register]()<br>
备注 : 查询当前所有的Agent信息

#### 请求参数

字段          |字段类型      |字段说明       |必须参数
--------------|------------|--------------|-------
client_id     |string      |客户端用户名    |是
client_secret |string      |客户端密钥      |是
page          |int         |页数           |是

#### 返回示例

```json  
{
    "status": 1,
    "state": "success",
    "message": [
        {
            "id":"1",
            "mac_addr": "34:36:3b:c9:1a:a0",
            "status": "0"
        },
        {
            "id":"2",
            "mac_addr": "e5:30:a3:72:3c:48",
            "status": "1"
        }
    ]
}
```

#### 返回参数

字段          |字段类型        |字段说明
--------------|--------------|-------
status        |int           |状态码
state         |string        |状态
message       |string        |备注信息
id            |int           |Agent ID
mac_addr      |string        |MAC地址
status        |int           |Agent状态，0为不可用，1为可用

#### 返回状态

状态码  |说明
--------|------------------------------
1       |请求成功
-1      |Client验证失败

---
> 请求方式 : POST<br>
请求URL : [http://47.101.186.138:5000/api/v1/register]()<br>
备注 : 新增Agent记录

#### 请求参数

字段           |字段类型     |字段说明       |必须参数
--------------|------------|--------------|-------
client_id     |string      |客户端用户名    |是
client_secret |string      |客户端密钥      |是
mac_addr      |string      |MAC地址        |是
status        |int         |Agent状态      |是

#### 返回示例

```json  
{
    "status": 1,
    "state": "success",
    "message": "Agent added"
}
```

#### 返回参数

字段          |字段类型        |字段说明
--------------|--------------|------------
status        |int           |状态码
state         |string        |状态
message       |string        |备注信息

#### 返回状态
状态码   |说明
--------|-----------
1       |新增注册记录成功
-1      |Client验证失败
-2      |已存在Agent记录

---
> 请求方式 : PUT<br>
请求URL : [http://47.101.186.138:5000/api/v1/register]()<br>
备注 : 修改Agent记录

#### 请求参数

字段           |字段类型     |字段说明       |必须参数
--------------|------------|--------------|-------
client_id     |string      |客户端用户名    |是
client_secret |string      |客户端密钥      |是
mac_addr      |string      |MAC地址        |是
status        |int         |Agent状态      |是

#### 返回示例

```json  
{
    "status": 1,
    "state": "success",
    "message": "Agent updated"
}
```

#### 返回参数

字段          |字段类型        |字段说明
--------------|--------------|------------
status        |int           |状态码
state         |string        |状态
message       |string        |备注信息

#### 返回状态
状态码   |说明
--------|-----------
1       |新增注册记录成功
-1      |Client验证失败
-2      |不存在Agent记录

---
> 请求方式 : DELETE<br>
请求URL : [http://47.101.186.138:5000/api/v1/register]()<br>
备注 : 删除Agent记录

#### 请求参数

字段           |字段类型     |字段说明       |必须参数
--------------|------------|--------------|-------
client_id     |string      |客户端用户名    |是
client_secret |string      |客户端密钥      |是
mac_addr      |string      |MAC地址        |是

#### 返回示例

```json  
{
    "status": 1,
    "state": "success",
    "message": "Agent deleted"
}
```

#### 返回参数

字段          |字段类型        |字段说明
--------------|--------------|------------
status        |int           |状态码
state         |string        |状态
message       |string        |备注信息

#### 返回状态
状态码   |说明
--------|-----------
1       |新增注册记录成功
-1      |Client验证失败
-2      |不存在Agent记录

---
### 2.Agent认证接口

#### 请求说明

> 请求方式 : GET<br>
请求URL : [http://47.101.186.138:5000/api/v1/auth]()<br>
备注 : Agent认证获取access_token

#### 请求参数

字段          |字段类型      |字段说明        |必须参数
--------------|------------|--------------|-------
mac_addr      |string      |MAC地址        |是

#### 返回示例

```json  
{
    "status": 1,
    "state": "success",
    "message": {
        "access_token": "MTU1NDgwMTY5MjowOmQwZTNiMGNlMDBiYzM4YTE5NTgwZWRlMjk4Y2RhOTUxYWM0YzBhODM="
    }
}
```

#### 返回参数

字段                    |字段类型       |字段说明
-----------------------|--------------|------------
status                 |int           |状态码
state                  |string        |状态
message                |string        |备注信息
access_token           |string        |access_token

#### 返回状态

状态码   |说明
--------|---------------------------
1       |Agent认证成功
-1      |Agent的MAC地址不在注册表

---
### 3.Agent心跳接口

#### 请求说明

> 请求方式 : GET<br>
请求URL : [http://47.101.186.138:5000/api/v1/heartbeat]()<br>
备注 : 查询Agent心跳记录

#### 请求参数

字段          |字段类型      |字段说明       |必须参数
--------------|------------|--------------|-------
client_id     |string      |客户端用户名    |是
client_secret |string      |客户端密钥      |是
mac_addr      |string      |MAC地址        |否
page          |int         |页数           |是

#### 返回示例

```json  
{
    "status": 1,
    "state": "success",
    "message": [
        {
            "mac_addr": "e5:30:a3:72:3c:48",
            "last_connection_time": "2018-12-07 14:15:16"
        }
    ]
}
```

#### 返回参数

字段                    |字段类型       |字段说明
-----------------------|--------------|------------
status                 |int           |状态码
state                  |string        |状态
message                |string        |备注信息
mac_addr               |string        |MAC地址
last_connection_time   |string        |最后连接时间

#### 返回状态

状态码   |说明
--------|---------------------------
1       |心跳包发送成功
-1      |Client验证失败

---
> 请求方式 : POST<br>
请求URL : [http://47.101.186.138:5000/api/v1/heartbeat]()<br>
备注 : 发送Agent心跳记录

#### 请求参数

字段         |字段类型      |字段说明       |必须参数
-------------|------------|--------------|-------
mac_addr     |string      |MAC地址        |是
access_token |string      |注册获取的令牌   |是
create_time  |string      |发送心跳包的时间 |是

#### 返回示例

```json  
{
    "status": 1,
    "state": "success",
    "message": "Server online"
}
```

#### 返回参数

字段           |字段类型       |字段说明
--------------|--------------|------------
status        |int           |状态码
state         |string        |状态
message       |string        |备注信息

#### 返回状态

状态码   |说明
--------|---------------------------
1       |心跳包发送成功
-1      |Agent验证失败
-2      |acess_token过期

---
### 4.Agent设备资源信息接口

#### 请求说明

> 请求方式 : GET<br>
请求URL : [http://47.101.186.138:5000/api/v1/resource]()<br>
备注 : 查询Agent心跳记录

#### 请求参数

字段          |字段类型      |字段说明       |必须参数
--------------|------------|--------------|-------
client_id     |string      |客户端用户名    |是
client_secret |string      |客户端密钥      |是
mac_addr      |string      |MAC地址        |是
page          |int         |页数           |是

#### 返回示例

```json  
{
    "status": 1,
    "state": "success",
    "message": [
        {
            "mac_addr": "00:00:00:00:00:00",
            "cpu_percent": 28.31,
            "cpu_count": 2,
            "cpu_freq_current": 76,
            "total_memory": 2048,
            "available_memory": 748,
            "sensors_battery_percent": 88,
            "boot_time": "2018-11-30 14:15:16",
            "create_time": "2018-11-01 23:41:25"
        }
    ]
}
```

#### 返回参数

字段                       |字段类型       |字段说明
--------------------------|--------------|------------
status                    |int           |状态码
state                     |string        |状态
mac_addr                  |string        |MAC地址
cpu_percent               |double        |CPU占用率
cpu_count                 |int           |CPU核心数
cpu_freq_current          |double        |CPU当前频率
total_memory              |int           |总内存
available_memory          |int           |可用内存
sensors_battery_percent   |double        |电池百分比
boot_time                 |string        |启动时间
create_time               |string        |记录时间

#### 返回状态

状态码   |说明
--------|---------------------------
1       |心跳包发送成功
-1      |Client验证失败

---

> 请求方式 : POST<br>
请求URL : [http://47.101.186.138:5000/api/v1/device_resource]()<br>
备注 : 发送Agent心跳记录

#### 请求参数

字段                    |字段类型      |字段说明        |必须参数
------------------------|------------|---------------|-------
mac_addr                |string      |MAC地址         |是
access_token            |string      |注册获取的令牌   |是
cpu_percent             |double      |CPU占用率       |否
cpu_count               |int         |CPU核心数       |否
cpu_freq_current        |double      |CPU当前频率     |否
cpu_freq_min            |double      |CPU最低频率     |否
cpu_freq_max            |double      |CPU最高频率     |否
total_memory            |int         |总内存          |否
available_memory        |int         |可用内存        |否
sensors_battery_percent |double      |电池电量百分比   |否
boot_time               |string      |系统启动时间     |否
create_time             |string      |发送心跳包的时间  |是

#### 返回示例

```json  
{
    "status": 1,
    "state": "success",
    "message": "Record added"
}
```

#### 返回参数

字段           |字段类型       |字段说明
--------------|--------------|------------
status        |int           |状态码
state         |string        |状态
message       |string        |备注信息

#### 返回状态

状态码   |说明
--------|---------------------------
1       |心跳包发送成功
-1      |Agent验证失败
-2      |acess_token过期

---
### 5.Agent信息推送接口

#### 请求说明

> 请求方式 : POST<br>
请求URL : [http://47.101.186.138:5000/api/v1/control]()<br>
备注 : 向Agent推送信息

#### 请求参数

字段            |字段类型      |字段说明         |必须参数
----------------|------------|----------------|-------
client_id       |string      |客户端用户名      |是
client_secret   |string      |客户端密钥        |是
mac_addr        |string      |MAC地址          |是
message         |string      |待推送信息        |是
create_time     |string      |发送时间         |是

#### 返回示例

```json  
{
    "status": 1,
    "state": "success",
    "message": "Message pushed successfully"
}
```

#### 返回参数

字段           |字段类型       |字段说明
--------------|--------------|------------
status        |int           |状态码
state         |string        |状态
message       |string        |备注信息

#### 返回状态

状态码   |说明
--------|-------------------------------
1       |心跳包发送成功
-1      |Client验证失败