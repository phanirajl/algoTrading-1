#!/usr/bin/env python
__author__ = "Lutz Künneke"
__copyright__ = ""
__credits__ = []
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lutz Künneke"
__email__ = "lutz.kuenneke89@gmail.com"
__status__ = "Prototype"
"""
Three Ducks Trend Following as found on BabyPips - Runner script
https://forums.babypips.com/t/the-3-ducks-trading-system/6430
Use at own risk
Author: Lutz Kuenneke, 12.07.2018
"""

from algoTrader.controller import controller
cont = controller('/home/ubuntu/settings_triangle.conf','live')
#allowed_ins = [ins.name for ins in cont.allowed_ins]
allowed_ins = ['XCU_USD',
               'WHEAT_USD',
               'CORN_USD',
               'USD_JPY',
               'USD_CAD',
               'EUR_USD',
               'EUR_CHF',
               'GBP_USD',
               'AUD_USD',
               'AUD_CHF',
               'AUD_JPY',
               'EUR_JPY',
               'BCO_USD',
               'WTICO_USD',
               'CAD_JPY',
               'GBP_AUD',
               'GBP_ZAR',
               'GBP_JPY',
               'NZD_USD',
               'NZD_CHF',
               'USD_CHF',
               'NATGAS_USD',
               'SOYBN_USD',
               'USD_CNH',
               'NZD_JPY',
               'GBP_ZAR',
               'SUGAR_USD',
               'ZAR_JPY',
               'USD_MXN',
               'EUR_CAD',
               'EUR_GBP',
               'EUR_AUD',
               'EUR_NZD',
               'USD_TRY',
               'EUR_TRY']
returns = [cont.checkIns(ins) for ins in allowed_ins]
