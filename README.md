gameServer
==========

some game server service like rank service


1����Ϸ��������
---------------

���ݿ�ʹ��redis

a.ע�ᣨgameCode���ǳƣ��豸id���û�id��userId����Ϊ��

register?gameCode=&version=&nickname=&deviceId=&userId=


b.�������

rank?gameCode=&version=&deviceId=&userId=

���:[{"nickname":"","score":100}]


c.�ύ����

commitScore?gameCode=&version=&deviceId=&userId=&score=