import datetime
from .translate import translate

from hashlib import *
import math

import string
digs = string.digits + string.ascii_letters

import requests
import json
# def getIp():
# 	request = requests.get('https://api.myip.com/')
# 	ip = json.loads(request.content)['ip']

# 	return ip

def int2base(x, base):
    if x < 0:
        sign = -1
    elif x == 0:
        return digs[0]
    else:
        sign = 1

    x *= sign
    digits = []

    while x:
        digits.append(digs[int(x % base)])
        x = int(x / base)

    if sign < 0:
        digits.append('-')

    digits.reverse()

    return ''.join(digits)

def hash(date, pseudo, ip, score):
	m = sha224()
	m.update(str(str(date) + str(pseudo) + str(ip) + str(score)).encode())
	return m.hexdigest()

def makeToken(payload, scoreToBase, ip):
	date  = datetime.date.today()
	# get ip from django
	has = hash(date, payload['username'], ip, payload['score'])

	chunkSize = len(scoreToBase)//3
	scoreChunks = [scoreToBase[:chunkSize], scoreToBase[chunkSize:chunkSize*2], scoreToBase[chunkSize*2:]]

	has = list(has)
	has[25] = scoreChunks[2]
	has[31] = scoreChunks[0]
	has[48] = scoreChunks[1]
	has[3] = scoreChunks[1]

	return ''.join(has)

def isCorrect(payload, ip):
	day =  datetime.date.today().day
	base = math.floor(translate(day,1,31,15,34))
	scoreToBase = int2base(payload['score'],base)

	correctToken = makeToken(payload, scoreToBase, ip)
	return payload['token'] == correctToken