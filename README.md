gameServer
==========

some game server service like rank service


1、游戏排名服务
---------------

数据库使用redis

a.注册（gameCode，昵称，设备id，用户id）userId可以为空

register?gameCode=&version=&nickname=&deviceId=&userId=
结果:{"code":200}


b.获得世界排名，不在前10没有名次

rank?gameCode=&version=&deviceId=&userId=
结果:{"code":200,"ranks":[{"nickname":"","score":100}]}


c.提交分数

commitScore?gameCode=&version=&deviceId=&userId=&score=
结果:{"ranks": [{"score": 1, "nickname": "test", "deviceId": "test1"}], "code": 200, "isEnterWorldRank": 1, "myWorldRank": 1}