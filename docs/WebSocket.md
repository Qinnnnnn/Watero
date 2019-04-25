### 1.Agent身份认证接口
Agent服务发送身份认证信息

#### 请求说明
> 请求方式 : WebSocket<br>
请求URL : [http://47.101.186.138:5001]()<br>
备注 : WebSocket数据通道Agent认证

#### 请求文本
```json
{
    "mac_addr": "34:36:3b:c9:1a:a0"
}
```

#### 返回示例
```json  
{
    "status":1,
    "state":"success",
    "message":"Identify successfully"
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
--------|---------------------------------------------
1       |身份认证成功
-1      |身份认证失败