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

from threeducks.controller import controller
# just some currencies that have been trending a few times in the past imho
#allowed_ins = ['EUR_USD', 'GBP_USD', 'USD_CAD', 'AUD_USD', 'USD_JPY', 'EUR_JPY']
## add some commodities
#allowed_ins.append('WHEAT_USD')
#allowed_ins.append('CORN_USD')
#allowed_ins.append('SOYBN_USD')
cont = controller('/home/ubuntu/settings_threeducks.conf')
allowed_ins = [ins.name for ins in cont.allowed_ins]
returns = [cont.checkIns(ins) for ins in allowed_ins]
