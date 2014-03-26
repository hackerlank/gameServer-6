# -*-encoding:utf-8-*-
'''
Copyright(c)2013,zhangchunsheng,www.zhangchunsheng.me
Version: 1.0
Author: zhangchunsheng
Date: 2014-03-26
Description: views
Modification:
	甲、乙、丙、丁、戊、己、庚、辛、壬、癸 甲（jiǎ）、乙（yǐ）、丙（bǐng）、丁（dīng）、戊（wù）、己（jǐ）、庚（gēng）、辛（xīn）、壬（rén）、癸（guǐ）
	子、丑、寅、卯、辰、巳、午、未、申、酉、戌、亥 子（zǐ）、丑（chǒu）、寅（yín）、卯（mǎo）、辰（chén）、巳（sì）、午（wǔ）、未（wèi）、申（shēn）、酉（yǒu）、戌（xū）、亥（hài）
	甲午年（马年）丁卯月丙申日 农历二月廿六
'''
import json;
import redis;
import time;

from django.http import Http404;
from django.shortcuts import render, get_object_or_404;
from django.http import HttpResponseRedirect, HttpResponse;
from django.template import RequestContext, loader;
from django.core.urlresolvers import reverse;
from django.views import generic;
from django.utils import timezone;

r = redis.StrictRedis(host='222.126.242.105', port='6379', db=6);#redis-py处理连接池
# Create your views here.
def index(request):
	r.set("foo", 'bar');
	foo = r.get("foo");
	return HttpResponse("index" + foo);
	
'''
注册（gameCode，昵称，设备id，用户id）userId可以为空
register?gameCode=test&version=&deviceId=test1&nickname=test&userId=

数据库结构
G_{gameCode}_D_{$deviceId} hash
gameCode version nickname deviceId userId registerDate
'''
def register(request):
	result = "";
	gameCode = "";
	version = "";
	deviceId = "";
	nickname = "";
	userId = "";
	if('gameCode' in request.GET):
		gameCode = request.GET["gameCode"];
	if('version' in request.GET):
		version = request.GET["version"];
	if('deviceId' in request.GET):
		deviceId = request.GET["deviceId"];
	if('nickname' in request.GET):
		nickname = request.GET["nickname"];
	if('userId' in request.GET):
		userId = request.GET["userId"];
	if(gameCode == "" or deviceId == "" or nickname == ""):
		result = {
			'code': 102,
			'message': 'argument exception'
		};
	else:
		#r = redis.StrictRedis(host='222.126.242.105', port='6379', db=6);
		#gameCode version nickname deviceId userId registerDate
		key = "G_" + gameCode + "_D_" + deviceId;
		if(r.exists(key)):
			result = {
				'code': 103,
				'message': 'exists device'
			};
		else:
			pipe = r.pipeline();
			pipe.hset(key, "gameCode", gameCode);
			pipe.hset(key, "version", version);
			pipe.hset(key, "nickname", nickname);
			pipe.hset(key, "deviceId", deviceId);
			pipe.hset(key, "userId", userId);
			date = int(time.time());
			pipe.hset(key, "registerDate", date);
			pipe.execute();
			result = {
				'code': 200
			};
	return HttpResponse(json.dumps(result));
	
'''
获得世界排名
rank?gameCode=test&version=
结果:{"code":200,"ranks":[{"nickname":"","score":100}]}

用户分数
用户排行，只保存分数最高的记录，如果没有nickname则为unname
G_{gameCode}_D_{$deviceId}_score list element:{"nickname":"","score":100}
rpush
lrange

世界排行
只保存前10名分数最高的玩家信息，如果没有nickname则为unname
G_{gameCode}_world list element:{"nickname":"","score":100}
rpush
lrange
'''
def rank(request):
	result = "";
	gameCode = "";
	version = "";
	if('gameCode' in request.GET):
		gameCode = request.GET["gameCode"];
	if('version' in request.GET):
		version = request.GET["version"];
	if(gameCode == ""):
		result = {
			'code': 102,
			'message': 'argument exception'
		};
	else:
		#r = redis.StrictRedis(host='222.126.242.105', port='6379', db=6);
		#gameCode version nickname deviceId userId registerDate
		key = "G_" + gameCode + "_world";
		if(r.exists(key)):
			ranks = r.lrange(key, 0, -1);
			world_ranks = [];
			for rank in ranks:
				world_ranks.append(json.loads(rank));
				
			result = {
				'code': 200,
				'ranks': world_ranks
			};
		else:
			result = {
				'code': 200,
				'ranks': []
			}
	return HttpResponse(json.dumps(result));
	

	
def saveScore(key, deviceId, nickname, currentScore):
	result = {};
	if(r.exists(key)):
		ranks = [];
		scores = r.lrange(key, 0, -1);
		for score in scores:
			ranks.append(json.loads(score));
		if(len(ranks) < 10):
			index = 0;
			for rank in ranks:
				if(currentScore >= rank["score"]):
					break;
				index += 1;
			value = {
				'deviceId': deviceId,
				'nickname': nickname,
				'score': currentScore
			};
			ranks.insert(index, value);
			r.linsert(key, "before", scores[index], json.dumps(value));
			result['isEnterRank'] = 1;
			result['myRank'] = index + 1;
			result['ranks'] = ranks;
		else:
			flag = False;
			index = 0;
			for rank in ranks:
				if(currentScore >= rank["score"]):
					flag = True;
					break;
				index += 1;
			value = {
				'deviceId': deviceId,
				'nickname': nickname,
				'score': currentScore
			};
			if(flag):
				ranks.insert(index, value);
				ranks.pop();
				r.linsert(key, "BEFORE", json.dumps(ranks[index]), json.dumps(value));
				r.rpop(key);
				result['isEnterRank'] = 1;
				result['myRank'] = index + 1;
				result['ranks'] = ranks;
			else:
				result['isEnterRank'] = 0;
				result['myRank'] = 0;
				result['ranks'] = ranks;
	else:
		value = {
			'deviceId': deviceId,
			'nickname': nickname,
			'score': currentScore
		};
		r.rpush(key, json.dumps(value));
		result['isEnterRank'] = 1;
		result['myRank'] = 1;
		result['ranks'] = [value];
	return result;
		
'''
提交分数
commitScore?gameCode=test&version=&deviceId=test1&userId=&score=1

用户分数
用户排行，只保存分数最高的记录，如果没有nickname则为unname
G_{gameCode}_D_{$deviceId}_score list element:{"nickname":"","score":100}
rpush
lrange

世界排行
只保存前10名分数最高的玩家信息，如果没有nickname则为unname
G_{gameCode}_world list element:{"nickname":"","score":100}
rpush
lrange
'''
def commitScore(request):
	result = "";
	gameCode = "";
	version = "";
	deviceId = "";
	userId = "";
	score = 0;
	if('gameCode' in request.GET):
		gameCode = request.GET["gameCode"];
	if('version' in request.GET):
		version = request.GET["version"];
	if('deviceId' in request.GET):
		deviceId = request.GET["deviceId"];
	if('userId' in request.GET):
		userId = request.GET["userId"];
	if('score' in request.GET):
		score = request.GET["score"];
	if(gameCode == "" or deviceId == "" or score == 0):
		result = {
			'code': 102,
			'message': 'argument exception'
		};
		return HttpResponse(json.dumps(result));
	if(not score.isdigit()):
		result = {
			'code': 102,
			'message': 'argument exception'
		};
		return HttpResponse(json.dumps(result));
		
	score = int(score);
		
	#r = redis.StrictRedis(host='222.126.242.105', port='6379', db=6);
	#lrange G_test_world 0 -1
	
	#先获得nickname
	nickname = "";
	key = "G_" + gameCode + "_D_" + deviceId;
	if(r.exists(key)):
		nickname = r.hget(key, "nickname");
		if(nickname == ""):
			nickname = "unname";
	else:
		nickname = "unname";
		
	#保存用户分数
	key_score = key + "_score";
	saveScore(key_score, deviceId, nickname, score);
	
	#查看世界排行
	key_world = "G_" + gameCode + "_world";
	isEnterWorldRank = 0;
	ranks = [];
	world_rankInfo = saveScore(key_world, deviceId, nickname, score);
	result = {
		'code': 200,
		'isEnterWorldRank': world_rankInfo['isEnterRank'],
		'myWorldRank': world_rankInfo['myRank'],
		'ranks': world_rankInfo['ranks']
	};
	return HttpResponse(json.dumps(result));