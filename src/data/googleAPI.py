#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
#
#	Name    : googleSheet
#	Author  : Ting
#   Version : 1
#   Purpose : A helper class to add Google API functions
#
###############################################################################

# Import Standard Packages 
from collections import defaultdict
import logging
import traceback
import requests
import pprint

# Import 3rd Party Packages 
import gspread

# Initiate Objects
log = logging.getLogger(name=__file__)


class googleSheet: 
    def __init__(self): 
        pass 


gc = gspread.service_account(filename='src/utils/_cred.json')
print(gc)
url = "https://docs.google.com/spreadsheets/d/1Dvi03zxigaUGx2Owpt8JPt5_pxR1I44bEhwEyQtsKJk/edit#gid=0"
# wks = gc.open("TrenDBase_Test").sheet1

# Open a sheet from a spreadsheet in one go
wks = gc.open_by_key('1Dvi03zxigaUGx2Owpt8JPt5_pxR1I44bEhwEyQtsKJk').sheet1
print(wks)


if __name__ == '__main__':
    pass 
