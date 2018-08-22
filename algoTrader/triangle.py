#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Lutz Künneke"
__copyright__ = ""
__credits__ = []
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lutz Künneke"
__email__ = "lutz.kuenneke89@gmail.com"
__status__ = "Prototype"
"""
Places orders to trade the triangle
Use at own risk
Author: Lutz Kuenneke, 12.07.2018
"""
import json
import time
import v20
from v20.request import Request
import requests
import configparser
import code
import math
import datetime
import numpy as np


class indicator(object):
 def __init__(self, controller):
  self.minbars = 5
  self.controller = controller
 def getTriangle(self,ins,granularity,numCandles,spread):
  if numCandles < self.minbars:
   return None
  candles = self.controller.getCandles(ins,granularity,numCandles)
  if not candles:
   return None
  upperFractals = []
  lowerFractals = []
  fractRange = 2
  highs = [candle.get('ask').get('h') for candle in candles[:-1]]
  lows = [candle.get('bid').get('l') for candle in candles[:-1]]
  x = len(candles) #datetime.datetime.strptime(candles[-1].get('time').split('.')[0],'%Y-%m-%dT%H:%M:%S')
  # get the upper line 
  y1 = 0.0
  mbest = -math.inf
  fupper = None
  n = 0
  for candle in candles:
   if float(candle.get('ask').get('h')) >= y1:
    x1 = n # datetime.datetime.strptime(candle.get('time').split('.')[0],'%Y-%m-%dT%H:%M:%S')
    y1 = float(candle.get('ask').get('h'))
    mbest = -math.inf
    fupper = None
    confirmed = False
   else:
    x2 = n # datetime.datetime.strptime(candle.get('time').split('.')[0],'%Y-%m-%dT%H:%M:%S')
    y2 = float(candle.get('ask').get('h'))
    tdelta = x2 - x1
    mup = (y2-y1)/float(tdelta)
    if mup > mbest:
     mbest = mup
     fupper = y1 + float(x-x1)*mup
     confirmed = False
     nc = 0
     for cc in candles:
      if nc == x1 or nc == x2:
       continue
      festim = y1 + float(nc-x1)*mup
      if festim - float(cc.get('ask').get('h')) < 5*spread:
       confirmed = True
      nc += 1
   n += 1
  # get the lower line
  y1 = math.inf
  mbest = math.inf
  flower = None
  n = 0
  for candle in candles:
   if float(candle.get('bid').get('l')) <= y1:
    x1 = n# datetime.datetime.strptime(candle.get('time').split('.')[0],'%Y-%m-%dT%H:%M:%S')
    y1 = float(candle.get('bid').get('l'))
    mbest = math.inf
    flower = None
    confirmedl = False
   else:
    x2 = n#  datetime.datetime.strptime(candle.get('time').split('.')[0],'%Y-%m-%dT%H:%M:%S')
    y2 = float(candle.get('bid').get('l'))
    tdelta = x2 - x1
    mup = (y2-y1)/float(tdelta)
    if mup < mbest:
     mbest = mup
     flower = y1 + float(x-x1)*mup
     confirmedl = False
     nc = 0
     for cc in candles:
      if nc == x1 or nc == x2:
       continue
      festim = y1 + float(nc-x1)*mup
      if float(cc.get('bid').get('l')) - festim < 5*spread:
       confirmedl = True
      nc += 1
   n += 1
  #print(ins + ' ' + str(flower) + ' ' + str(fupper))
  if not fupper or not flower or not confirmed or not confirmedl:
   return self.getTriangle(ins,granularity,numCandles-1,spread)
  
  return [flower, fupper]

 def checkIns(self, ins):
  if len([trade for trade in self.controller.trades if trade.instrument == ins]) > 0:
   print('Skipping ' + ins + ' found open trade')
   return None
  price = self.controller.getPrice(ins)
  spread = self.controller.getSpread(ins)
  pipLoc = self.controller.getPipSize(ins)
  pipVal = 10 ** (-pipLoc + 1)
  moveout = 2
  granularity = 'D'
  numCandles = 40
  triangle = self.getTriangle(ins,granularity,numCandles,0.0005*price)
  if not triangle:
   #triangle = self.getTriangle(ins,'H4',180,spread)
   #if not triangle:
   return None # could not get triangle formation
  
  upperentry = triangle[1]+moveout*spread
  lowerentry = triangle[0]-moveout*spread
  sl = (triangle[1]+triangle[0])/2
  tpupper = upperentry + (upperentry - sl)/0.618 # some serious FIB stuff
  tplower = lowerentry + (lowerentry - sl)/0.618 # some serious FIB stuff
  upperunits = self.controller.getUnits(abs(sl-upperentry),ins)
  lowerunits = -self.controller.getUnits(abs(sl-lowerentry),ins)
  if price > upperentry or price < lowerentry or upperunits == 0 or lowerunits == 0:
   print('Skipping ' + ins + '. ' + str(price) + ' ' + str(upperentry) + ' ' + str(lowerentry) + ' ' + str(upperunits) + ' ' + str(lowerunits))
   return None # skip if not inside triangle

  fstr = '30.' + str(pipLoc) + 'f'
  tpupper = format(tpupper, fstr).strip()
  tplower = format(tplower, fstr).strip()
  sl = format(sl, fstr).strip()
  #sldist = format(sldist, fstr).strip()
  upperentry = format(upperentry, fstr).strip()
  lowerentry = format(lowerentry, fstr).strip()
  expiry = datetime.datetime.now() + datetime.timedelta(days=1)
  args = {'order': {
      'instrument': ins,
      'units': upperunits,
      'price': upperentry,
      'type': 'STOP',
      'timeInForce': 'GTD',
      'gtdTime': expiry.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
      'takeProfitOnFill': {'price': tpupper, 'timeInForce': 'GTC'},
      'stopLossOnFill': {'price': sl, 'timeInForce': 'GTC'},
      }}
  ticket = self.controller.oanda.order.create(self.controller.settings.get('account_id'
          ), **args)
  ticket_json = json.loads(ticket.raw_body)
  print(ticket_json)
  args = {'order': {
      'instrument': ins,
      'units': lowerunits,
      'price': lowerentry,
      'type': 'STOP',
      'timeInForce': 'GTD',
      'gtdTime': expiry.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
      'takeProfitOnFill': {'price': tplower, 'timeInForce': 'GTC'},
      'stopLossOnFill': {'price': sl, 'timeInForce': 'GTC'},
      }}
  ticket = self.controller.oanda.order.create(self.controller.settings.get('account_id'
          ), **args)
  ticket_json = json.loads(ticket.raw_body)
  print(ticket_json)