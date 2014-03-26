gameServer
==========

some game server service like rank service


1、游戏排名服务
---------------

数据库使用redis

a.注册（gameCode，昵称，设备id，用户id）userId可以为空

register?gameCode=&version=&nickname=&deviceId=&userId=


b.获得排名

rank?gameCode=&version=&deviceId=&userId=

结果:[{"nickname":"","score":100}]


c.提交分数

commitScore?gameCode=&version=&deviceId=&userId=&score=