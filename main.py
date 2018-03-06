#!/usr/bin/python3
import os
import sys
import time
import json
from urllib.request import urlopen

import analyzer
import self_functions

os.system("clear")

#-------------------------------------------------------------------------------
print("Script Info".center(110,"*"))
print("Script_Name:",sys.argv[0])
for i in range(1,len(sys.argv)):
    print("Arg",i,"",sys.argv[i])

#-------------------正式开始-----------------------------------------------------

print("\n","Summoner Info".center(110,"*"))
try:
    summoner_dict = self_functions.Request_summoner_name(sys.argv[1])
except:
    print("Summoner Info ERROR")
else:
    for a in summoner_dict:
        print(a,":",summoner_dict[a])


print("\n","Current match".center(110,"*"))
#Request_current()
try:
    current_str = Request_current()
except:
    print(sys.argv[1],"is not in game")
else:
    print(summoner_dict["name"]+" is in the game")







print("\n","Recent matches".center(110,"*"))
matches_list = self_functions.Request_matches()
report = analyzer.matches_reporter()

for a in range(len(matches_list["matches"])):
    match_dict = self_functions.Request_match(str(matches_list["matches"][a]["gameId"]))

    match = analyzer.match_analyzer(match_dict,summoner_dict["name"])
    #把每一场的关键信息（match。export（）导出，由report.rattacher（）导入）
    report.rattacher(match.export())
    if len(sys.argv) > 2 :
        match.display_all()
    else:
        match.display()

report.analyze()

report.output()














print("\n\n","Script End".center(110,"*"))
