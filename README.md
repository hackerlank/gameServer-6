gameServer
==========

some game server service like rank service


1����Ϸ��������
---------------

���ݿ�ʹ��redis

a.ע�ᣨgameCode���ǳƣ��豸id���û�id��userId����Ϊ��

register?gameCode=&version=&nickname=&deviceId=&userId=
���:{"code":200}


b.�����������������ǰ10û������

rank?gameCode=&version=&deviceId=&userId=
���:{"code":200,"ranks":[{"nickname":"","score":100}]}


c.�ύ����

commitScore?gameCode=&version=&deviceId=&userId=&score=
���:{"ranks": [{"score": 1, "nickname": "test", "deviceId": "test1"}], "code": 200, "isEnterWorldRank": 1, "myWorldRank": 1}

���Ϸ�����

1��ע��

http://222.126.242.105:8080/wsgi/rankService/register?gameCode=test&version=&deviceId=test1&nickname=test&userId=

2�������������

http://222.126.242.105:8080/wsgi/rankService/rank?gameCode=test&version=

3���ύ����

http://222.126.242.105:8080/wsgi/rankService/commitScore?gameCode=test&version=&deviceId=test1&userId=&score=1