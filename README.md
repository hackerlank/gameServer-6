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