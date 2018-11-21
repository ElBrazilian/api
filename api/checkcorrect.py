import datetime
from translate import translate

from hashlib import *
import math

import string
digs = string.digits + string.ascii_letters

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

def makeToken(payload, scoreToBase):
	date  = datetime.date.today()
	# get ip from django
	ip = '78.247.42.62'
	has = hash(date, payload['username'], ip, payload['score'])

	chunkSize = len(scoreToBase)//3
	scoreChunks = [scoreToBase[:chunkSize], scoreToBase[chunkSize:chunkSize*2], scoreToBase[chunkSize*2:]]

	has = list(has)
	has[25] = scoreChunks[2]
	has[31] = scoreChunks[0]
	has[48] = scoreChunks[1]
	has[3] = scoreChunks[1]

	return ''.join(has)

def isCorrect(payload):
	day =  datetime.date.today().day
	base = math.floor(translate(day,1,31,15,34))
	scoreToBase = int2base(payload['score'],base)

	correctToken = makeToken(payload, scoreToBase)
	return payload['token'] == correctToken