import time
import self_functions
import re

class player:
    def __init__(self,index,match_dict):
        self.summonerId = match_dict.get("participantIdentities")[index].get("player").get("accountId")
        #match_dict["participantIdentities"][index]["player"]["summonerId"]
        self.accountId = match_dict.get("participantIdentities")[index].get("player").get("accountId")
        self.name = match_dict.get("participantIdentities")[index].get("player").get("summonerName")
#基本信息
        if index < 5:
            self.team = 0
        else:
            self.team = 1
        self.result = match_dict["teams"][self.team]["win"]
        self.champion = self_functions.get_champion_name(
            match_dict["participants"][index]["championId"]
            )+":"+str(match_dict["participants"][index]["championId"
            ])
        if (match_dict.get("participants")[index].get("timeline").get("lane") == "NONE" or match_dict.get("participants")[index].get("timeline").get("lane") == "BOTTOM" ):
            self.lane = match_dict.get("participants")[index].get("timeline").get("role")
        else:
            self.lane = match_dict.get("participants")[index].get("timeline").get("lane")
        self.kills = match_dict["participants"][index]["stats"]["kills"]
        self.deaths = match_dict["participants"][index]["stats"]["deaths"]
        self.assists = match_dict["participants"][index]["stats"]["assists"]
        self.KDA_str = str(self.kills)+"-"+str(self.deaths)+"-"+str(self.assists)
        self.KDA = round((self.kills + self.assists * 0.5)/(self.deaths + 1),1)
        self.farm = match_dict["participants"][index]["stats"]["totalMinionsKilled"] + match_dict["participants"][index]["stats"].get("neutralMinionsKilled")
        self.spell = [
            self_functions.get_spell_name(match_dict["participants"][index]["spell1Id"]),
            self_functions.get_spell_name(match_dict["participants"][index]["spell2Id"])
            ]
        self.items = [
            self_functions.get_item_name(match_dict["participants"][index]["stats"]["item0"]),
            self_functions.get_item_name(match_dict["participants"][index]["stats"]["item1"]),
            self_functions.get_item_name(match_dict["participants"][index]["stats"]["item2"]),
            self_functions.get_item_name(match_dict["participants"][index]["stats"]["item3"]),
            self_functions.get_item_name(match_dict["participants"][index]["stats"]["item4"]),
            self_functions.get_item_name(match_dict["participants"][index]["stats"]["item5"])
            ]
#可分析信息
        self.dmg = match_dict["participants"][index]["stats"]["totalDamageDealtToChampions"]
        self.dmgtaken = match_dict["participants"][index]["stats"]["totalDamageTaken"]
        self.gold = match_dict["participants"][index]["stats"]["goldEarned"]
        self.wards_placed = match_dict.get("participants")[index].get("stats").get("wardsPlaced")
        self.wards_killed = match_dict.get("participants")[index].get("stats").get("wardsKilled")
        self.vision_score = match_dict["participants"][index]["stats"]["visionScore"]
        self.living = match_dict["participants"][index]["stats"]["longestTimeSpentLiving"]
        self.multikill = match_dict["participants"][index]["stats"]["largestMultiKill"]

    def set_teamtotal(self,dmg,dmgtaken,gold):
        self.dmg_rate = round(self.dmg / dmg,2)
        self.dmgtaken_rate = round(self.dmgtaken / dmgtaken,2)
        self.gold_rate = round(self.gold / gold,2)

    def show(self):
        print(
            self.name.center(20),self.champion.center(14),
            self.KDA_str.center(8),"farm:",str(self.farm).ljust(3),self.lane.center(15),self.result.center(6),
            self.KDA
        )

    def show_all(self):
        print(
            self.name.center(20,"~"),self.champion.center(14),
            self.KDA_str.center(8),"farm:",str(self.farm).ljust(3),self.lane.center(15),self.result,
            "\n",self.spell[0].center(10),"|",self.items[0].center(25),"|",self.items[1].center(25),"|",self.items[2].center(25),"|",
            "\n",self.spell[1].center(10),"|",self.items[3].center(25),"|",self.items[4].center(25),"|",self.items[5].center(25),"|",
            "\n","Dmg:",self.dmg_rate,"\t","Taken",self.dmgtaken_rate,"\t","Gold",self.gold_rate,"\t",
            "\n","Vision:",self.wards_placed,self.wards_killed,"VisionScore:".rjust(10),self.vision_score,
        )



class match_analyzer:

    def __init__(self,match_dict,target):
        self.match_dict = match_dict
        self.date = time.strftime("%Y-%m-%d %H:%M", time.localtime(int(match_dict["gameCreation"])/1000))
        self.duration = self.match_dict["gameDuration"]
        self.gameId = self.match_dict["gameId"]
        self.blueteam = {
            "result":self.match_dict["teams"][0]["win"],
            "player":[],
            "totalDmg":0,
            "totalDmgTaken":0,
            "totalGold":0
        }
        self.redteam = {
            "result":self.match_dict["teams"][1]["win"],
            "player":[],
            "totalDmg":0,
            "totalDmgTaken":0,
            "totalGold":0
        }

        for index in range(0,5):
            self.redteam["player"].append(player(index+5,self.match_dict))
            self.redteam["totalDmg"] = self.redteam["totalDmg"] + self.redteam["player"][index].dmg
            self.redteam["totalDmgTaken"] = self.redteam["totalDmgTaken"] + self.redteam["player"][index].dmgtaken
            self.redteam["totalGold"] = self.redteam["totalGold"] + self.redteam["player"][index].gold
        for index in range(0,5):
            self.blueteam["player"].append(player(index,self.match_dict))
            self.blueteam["totalDmg"] = self.blueteam["totalDmg"] + self.blueteam["player"][index].dmg
            self.blueteam["totalDmgTaken"] = self.blueteam["totalDmgTaken"] + self.blueteam["player"][index].dmgtaken
            self.blueteam["totalGold"] = self.blueteam["totalGold"] + self.blueteam["player"][index].gold
#把团队伤害、承伤、经济总和传回给每个player
        for index in range(0,5):
            self.redteam["player"][index].set_teamtotal(
                self.redteam["totalDmg"],
                self.redteam["totalDmgTaken"],
                self.redteam["totalGold"]
            )
            self.blueteam["player"][index].set_teamtotal(
                self.blueteam["totalDmg"],
                self.blueteam["totalDmgTaken"],
                self.blueteam["totalGold"]
            )
#每一局的关键人物信息
            self.targetplayer = self.find_player(target)

    def display(self):
        self.targetplayer.show()

    def display_all(self):
        print("Game Details:\n",
            "Date:",self.date," ".ljust(10),"Duration:",self.duration//60,"m",self.duration%60,"s",self.gameId)
        print("Blue Team(100)".center(70,"-"))
        print("totalDmg:",self.blueteam["totalDmg"]," ".ljust(7),"totalDmgTaken:",self.blueteam["totalDmgTaken"]," ".ljust(7),"totalGold:",self.blueteam["totalGold"])
        for index in range(0,5):
            self.blueteam["player"][index].show_all()
        print("Red Team(200)".center(70,"-"))
        print("totalDmg:",self.redteam["totalDmg"]," ".ljust(7),"totalDmgTaken:",self.redteam["totalDmgTaken"]," ".ljust(7),"totalGold:",self.redteam["totalGold"])
        for index in range(0,5):
            self.redteam["player"][index].show_all()


    def find_player(self,name):
        for a in range(10):
            if re.match(name,self.match_dict["participantIdentities"][a]["player"]["summonerName"],re.I):
                if a > 4:
                    return self.redteam["player"][a-5]
                else:
                    return self.blueteam["player"][a]

    def export(self):
        return {"targetplayer":self.targetplayer,
                "gameId":self.gameId,
                "time":self.duration//60
                }


class matches_reporter:

    def __init__(self):
        self.info_list = []
        self.win_matches = []
        self.fail_matches = []

        self.win_rate = 0
        self.win_lane_rate = [0,0,0,0,0] #顺序分别为上，野，中，辅，AD
        self.fail_lane_rate = [0,0,0,0,0] #顺序分别为上，野，中，辅，AD
        self.win_avg_kda = 0
        self.fail_avg_kda = 0
        self.fb_win_rate = 0
        self.ft_win_rate = 0

    def rattacher(self,match_target):
        if (match_target.get("targetplayer").result == "Win"):
            self.win_matches.append(match_target)
        else:
            self.fail_matches.append(match_target)

    def analyze(self):
        self.win_rate = len(self.win_matches) / (len(self.win_matches)+len(self.fail_matches))
        for a in range(len(self.win_matches)):
            self.win_avg_kda += self.win_matches[a].get("targetplayer").KDA


            if(self.win_matches[a].get("targetplayer").lane == "TOP"):
                self.win_lane_rate[0]+=1
                continue
            elif(self.win_matches[a].get("targetplayer").lane == "JUNGLE"):
                self.win_lane_rate[1]+=1
                continue
            elif(self.win_matches[a].get("targetplayer").lane == "MIDDLE"):
                self.win_lane_rate[2]+=1
                continue
            elif(self.win_matches[a].get("targetplayer").lane == "DUO_SUPPORT"):
                self.win_lane_rate[3]+=1
                continue
            elif(self.win_matches[a].get("targetplayer").lane == "DUO_CARRY"):
                self.win_lane_rate[4]+=1
                continue

        self.win_avg_kda = round(self.win_avg_kda/len(self.win_matches),1)



        for a in range(len(self.fail_matches)):
            self.fail_avg_kda += self.fail_matches[a].get("targetplayer").KDA
            if(self.fail_matches[a].get("targetplayer").lane == "TOP"):
                self.fail_lane_rate[0]+=1
                continue
            elif(self.fail_matches[a].get("targetplayer").lane == "JUNGLE"):
                self.fail_lane_rate[1]+=1
                continue
            elif(self.fail_matches[a].get("targetplayer").lane == "MIDDLE"):
                self.fail_lane_rate[2]+=1
                continue
            elif(self.fail_matches[a].get("targetplayer").lane == "DUO_SUPPORT"):
                self.fail_lane_rate[3]+=1
                continue
            elif(self.fail_matches[a].get("targetplayer").lane == "DUO_CARRY"):
                self.fail_lane_rate[4]+=1
                continue

        self.fail_avg_kda = round(self.fail_avg_kda/len(self.fail_matches),1)

    def output(self):
        print(
            "\nwinrate:",str(self.win_rate *100) + "%","\n",
            "win_lane".center(14),"fail_lane".center(8),
            "\nTop：",self.win_lane_rate[0],"|".center(10),self.fail_lane_rate[0],
            "\nJgl：",self.win_lane_rate[1],"|".center(10),self.fail_lane_rate[1],
            "\nMid：",self.win_lane_rate[2],"|".center(10),self.fail_lane_rate[2],
            "\nSup：",self.win_lane_rate[3],"|".center(10),self.fail_lane_rate[3],
            "\nADC：",self.win_lane_rate[4],"|".center(10),self.fail_lane_rate[4],
            )
        print(
            "\nwin_avg_kda",self.win_avg_kda,
            "\nfail_avg_kda",self.fail_avg_kda,
        )
