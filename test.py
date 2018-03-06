#!/usr/bin/python3

import analyzer

import json
from urllib.request import urlopen
import sys
import time

html = urlopen("https://euw1.api.riotgames.com/lol/match/v3/matches/3529145029?api_key=RGAPI-0ec2da59-634a-4b5a-9020-fda3bc89fffe")
#html type: httpresponse
#type:httpresponse->byte->string->dictonary
match_dict = json.loads(html.read().decode())


report = analyzer.matches_reporter()

match = analyzer.match_analyzer(match_dict,"fanyizhe")
match.display_all()
print("\n\n")
match.targetplayer.show_all()
print("\n",match.targetplayer.summonerId)

report.rattacher(match.export())
report.analyze()
report.output()
