
#!/usr/bin/python3
import json
from urllib.request import urlopen
import sys
import time

API_KEY = "api_key=RGAPI-0ec2da59-634a-4b5a-9020-fda3bc89fffe"

def get_spell_name(spellId):
    with open ("./resource/summoner-spells.json","r") as ch:
        load_ch = json.load(ch)
        #print(load_ch["data"])
    for a in load_ch["data"]:
        if load_ch["data"][a]["id"] == spellId:
            return load_ch["data"][a]["name"]
            break

def get_champion_name(championId):
    with open ("./resource/champion.json","r") as ch:
        load_ch = json.load(ch)
        #print(load_ch["data"])
    for a in load_ch["data"]:
        if load_ch["data"][a]["id"] == championId:
            return a
            break
def get_item_name(itemId):
    with open ("./resource/items.json","r") as it:
        load_it = json.load(it)
    if itemId == 0:
        return " "
    else:
        for a in load_it["data"]:
            if load_it["data"][a]["id"] == itemId:
                return load_it["data"][a]["name"]
                break
        return "Not found"

def match_info(match_dict):
    print("Game Details","Duration:",match_dict["gameDuration"]//60,":",match_dict["gameDuration"]%60)
    print("Blue Team(100)".center(80,"-"),match_dict["teams"][0]["win"])
    for b in range(len(match_dict["participantIdentities"])):
        print(match_dict["participantIdentities"][b]["player"]["summonerName"].center(20,"^"),
            #str(match_dict["participants"][b]["championId"]).center(3),
            str(get_champion_name(match_dict["participants"][b]["championId"])).ljust(11),
            "KDA:",
                str(match_dict["participants"][b]["stats"]["kills"]).ljust(2),
                str(match_dict["participants"][b]["stats"]["deaths"]).ljust(2),
                str(match_dict["participants"][b]["stats"]["assists"]).ljust(2)
        )
        print("".rjust(20),end = " ")
        for c in ["item0","item1","item2"]:
            print(str(get_item_name(match_dict["participants"][b]["stats"][c])).ljust(25),end = "")
        print("\n","".rjust(20),end="")
        for c in ["item3","item4","item5"]:
            print(str(get_item_name(match_dict["participants"][b]["stats"][c])).ljust(25),end = "")
        print("")
        if b==4 :
            print("Red Team(200)".center(80,"-"),match_dict["teams"][1]["win"])

    print("\n")
#-------------------------------------------------------------------------------
def Request_summoner_name(summoner_name):
    part1 = "https://euw1.api.riotgames.com/lol/summoner/v3/summoners/by-name/"
    part2 = summoner_name;
    Request_summoner=part1+part2+"?"+API_KEY
    html = urlopen(Request_summoner) #html type: httpresponse
    #type:httpresponse->byte->string->dictonary
    global summoner_dict
    summoner_dict = json.loads(html.read().decode())
    summoner_dict.pop("revisionDate")
    return summoner_dict

def Request_matches():
    part1 = "https://euw1.api.riotgames.com/lol/match/v3/matchlists/by-account/"
    Request_matches = part1+str(summoner_dict["accountId"])+"/recent"+"?"+API_KEY
    #"/recent" can be added before API_KEY
    html = urlopen(Request_matches) #html type: httpresponse
    global matches_dict
    #type:httpresponse->byte->string->dictonary
    matches_dict = json.loads(html.read().decode())
    return matches_dict


def Request_match(gameId):
    part1 = "https://euw1.api.riotgames.com/lol/match/v3/matches/"
    Request_match = part1+gameId+"?"+API_KEY
    html = urlopen(Request_match) #html type: httpresponse
    global match_dict
    #type:httpresponse->byte->string->dictonary
    match_dict = json.loads(html.read().decode())
    return match_dict

def Request_current():
    part1 = "https://euw1.api.riotgames.com/lol/spectator/v3/active-games/by-summoner/"
    Request_current = part1+str(summoner_dict["id"])+"?"+API_KEY
    html = urlopen(Request_current) #html type: httpresponse
    global current_dict
    #type:httpresponse->byte->string->dictonary
    current_dict = json.loads(html.read().decode())
    return current_dict
