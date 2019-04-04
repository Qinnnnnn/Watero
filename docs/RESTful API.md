### 1.Agent注册接口

#### 请求说明

---
> 请求方式 : GET<br>
请求URL : [http://47.101.186.138:5000/api/v1/register]()<br>
备注 : 查询当前所有的Agent信息

#### 请求参数

字段          |字段类型      |字段说明       |必须参数
--------------|------------|--------------|-------
client_id     |string      |客户端用户名    |是
client_secret |string      |客户端密钥      |是
page          |string      |页数           |是

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
status        |string      |Agent状态      |是

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
status        |string      |Agent状态      |是

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

### 2.Agent心跳接口

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
page          |string      |页数           |是

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

### 3.Agent设备资源信息接口

Agent服务发送设备资源信息

#### 请求说明
> 请求方式 : POST<br>
请求URL : [http://47.101.186.138:5000/api/v1/device_resource]()

#### 请求参数
字段                    |字段类型      |字段说明       |必须参数
------------------------|------------|--------------|-------
mac_addr                |string      |MAC地址        |是
access_token            |string      |注册获取的令牌   |是
cpu_percent             |string      |CPU占用率       |否
cpu_count               |string      |CPU核心数       |否
cpu_freq_current        |string      |CPU当前频率     |否
cpu_freq_min            |string      |CPU最低频率     |否
cpu_freq_max            |string      |CPU最高频率     |否
total_memory            |string      |总内存          |否
available_memory        |string      |可用内存        |否
sensors_battery_percent |string      |电池电量百分比   |否
boot_time               |string      |系统启动时间     |否
create_time             |string      |发送心跳包的时间 |是

#### 返回示例
```json  
{
    "status": 1,
    "state": "success",
    "message": {
        "info": "Device resource record added"
    }
}
```

#### 返回参数
字段           |字段类型       |字段说明
--------------|--------------|------------
info          |string        |提示信息

#### 返回状态
状态码   |说明
--------|---------------------------
0       |MAC地址或access_token验证失败
1       |设备信息发送成功

---

### 4.Agent控制信息接口
Client发送控制信息

#### 请求说明
> 请求方式 : POST<br>
请求URL : [http://47.101.186.138:5000/api/v1/control]()

#### 请求参数
字段            |字段类型      |字段说明         |必须参数
----------------|------------|----------------|-------
access_id       |string      |分配的id         |是
access_secret   |string      |分配的secret     |是
mac_addr        |string      |MAC地址          |是
control         |string      |控制信息          |是
create_time     |string      |发送控制信息的时间 |是

#### 返回示例
```json  
{
    "status": 1,
    "state": "success",
    "message": {
        "info": "Control information was delivered successfully"
    }
}
```

#### 返回参数
字段           |字段类型       |字段说明
--------------|--------------|------------
info          |string        |提示信息

#### 返回状态
状态码   |说明
--------|-------------------------------
0       |access_id或access_secret验证失败
1       |控制信息发送成功