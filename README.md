# Chat_IPv6

## 功能

&ensp; 实现两台主机之间的文本聊天通信，通信在IPv6环境下进行,完成了登录和注册功能、点对点聊天、群聊等功能。

## 实现过程

### 基于UDP协议的Socket通信

&ensp; UDP是一个无连接协议，传输数据之前源端和终端不建立连接，当它想传送时就简单地去抓取来自应用程序的数据，并尽可能快地把它扔到网络上。  
&ensp; 通信协议层面主要用到的方法为：

    socket([family[, type[, proto]]])  
    bind(address: Union[_Address, bytes])  
    sendto(data, address,)
    recvfrom(bufsize, flags,)

### SQLite3数据库实现

&ensp; 在程序设计的过程中需要用到数据库来存储用户的用户名、密码、状态，用户IP地址和端口。在数据库选择的时候，用到的是SQLite3轻量级数据库，方便数据库的迁移等。  
  
| 函数名  | 功能    |
| :----:  | :----: |
| init(self) |  用来创建和打开数据库  |
| select_all(self) |用来获取数据库相应表中的所用用户信息|
|register(self, username, password, ip, port)|注册时调用，用于添加用户信息|
|search_username(self, username)| 根据用户名查找用户信息|
|login_success(self, username, ip, port)|登录成功后，更改数据库中的用户状态信息|
|login_check(self, username, password, ip, port)|登录时用于检查用户名和密码是否正确|
|logout_success(self, username)|在用户注销登陆时，更改用户的状态|
|db_close(self)|关闭数据库|  

## 运行测试

&ensp; 在两台可以通信的主机上分别进入代码所在目录，分别执行```python3 Client.py```和```python3 Server.py```。客户端可以根据需求实现多开，服务器只能开一个。在开启服务器的同时会打开数据库。  
&ensp; 根据提示，进行选择，可以实现不同的功能。在点对点聊天中，任意一方发送END，即可关闭聊天，另一方根据提示确认即可。群聊的实现原理类似，运行测试过程也类似。