import json
import math
import os
import shutil
import random

below_25_range = []
below_50_range = []
chance_6_range = []
chance_5_range = []
chance_4_range = []
chance_3_range = []
chance_2_range = []
stat_pool = []
stat = [
    "ZAN",
    "DAG",
    "TOT",
    "FLA",
    "ICE",
    "LIG",
    "HOL",
    "DAR"
]
second_stat = [
    "POI",
    "CUR",
    "STO",
    "SLO"
]
EXP_range = [34, 34, 34, 106, 0, 178, 274, 274, 394, 394, 394, 538, 706, 0, 898, 898, 1114, 1354, 1618, 2218, 2554, 0, 58, 1906]
log = []

#Content
with open("Data\\CharacterParameterMaster\\Content\\PB_DT_CharacterParameterMaster.json", "r", encoding="utf-8") as file_reader:
    content = json.load(file_reader)

#Data
with open("Data\\CharacterParameterMaster\\Translation.json", "r", encoding="utf-8") as file_reader:
    translation = json.load(file_reader)

for i in range(24):
    below_25_range.append(i+1)

for i in range(49):
    below_50_range.append(i+1)

for i in range(98):
    if i <= 49:
        for e in range(5):
            chance_6_range.append(i+1)
    else:
        chance_6_range.append(i+1)

for i in range(98):
    if i <= 49:
        for e in range(4):
            chance_5_range.append(i+1)
    else:
        chance_5_range.append(i+1)

for i in range(98):
    if i <= 49:
        for e in range(3):
            chance_4_range.append(i+1)
    else:
        chance_4_range.append(i+1)

for i in range(98):
    if i <= 49:
        for e in range(2):
            chance_3_range.append(i+1)
    else:
        chance_3_range.append(i+1)

for i in range(98):
    chance_2_range.append(i+1)

stat_int = -100.0
for i in range(41):
    for e in range(2**(int(abs(math.ceil(abs(stat_int)/25)-4)))):
        stat_pool.append(stat_int)
    stat_int += 5.0

def more_HP():
    content[5]["Value"]["MaxHP"] += 300
    content[5]["Value"]["MaxHP99Enemy"] += 300
    content[6]["Value"]["MaxHP"] += 300
    content[6]["Value"]["MaxHP99Enemy"] += 300
    content[10]["Value"]["MaxHP"] += 300

def zangetsu_stats():
    content[6]["Value"]["STR"] = 0.0
    content[6]["Value"]["INT"] = 0.0
    content[6]["Value"]["CON"] = 0.0
    content[6]["Value"]["MND"] = 0.0
    content[6]["Value"]["LUC"] = 0.0
    content[6]["Value"]["STR99Enemy"] = 0.0
    content[6]["Value"]["INT99Enemy"] = 0.0
    content[6]["Value"]["CON99Enemy"] = 0.0
    content[6]["Value"]["MND99Enemy"] = 0.0
    content[6]["Value"]["LUC99Enemy"] = 0.0

def zangetsu_EXP():
    i = 12
    while i <= 137:
        content[i]["Value"]["Experience99Enemy"] = 0
        content[i]["Value"]["Experience"] = 0
        i += 1
    i = 138
    while i <= 161:
        content[i]["Value"]["Experience99Enemy"] = EXP_range[i-138]
        content[i]["Value"]["Experience"] = EXP_range[i-138]
        i += 1

def rand_enemy(level, resist):
    #MainCastleEnemies
    i = 12
    while i <= 102:
        if resist and content[i]["Value"]["ZAN"] != 100.0:
            rand_stat(i)
        if level:
            if content[i]["Key"][0:5] == "N3006":
                patch_level(below_25_range, i)
            elif content[i]["Key"][0:5] == "N3025":
                patch_level(chance_2_range, i)
            else:
                patch_level(chance_6_range, i)
        i += 1
    #JapanEnemies
    i = 103
    while i <= 107:
        if resist and content[i]["Value"]["ZAN"] != 100.0:
            rand_stat(i)
        if level:
            patch_level(chance_5_range, i)
        i += 1
    #DenEnemies
    i = 108
    while i <= 121:
        if resist and content[i]["Value"]["ZAN"] != 100.0:
            rand_stat(i)
        if level:
            patch_level(chance_4_range, i)
        i += 1
    #IceEnemies
    i = 122
    while i <= 129:
        if resist and content[i]["Value"]["ZAN"] != 100.0:
            rand_stat(i)
        if level:
            patch_level(chance_3_range, i)
        i += 1
    #BackerBosses
    i = 130
    while i <= 137:
        if resist and content[i]["Value"]["ZAN"] != 100.0:
            rand_stat(i)
        if level:
            patch_level(chance_3_range, i)
        i += 1
    #MainCastleBosses
    i = 138
    while i <= 156:
        if resist and content[i]["Value"]["ZAN"] != 100.0:
            rand_stat(i)
        if level:
            if content[i]["Key"][0:5] == "N1001":
                patch_level(below_25_range, i)
            elif content[i]["Key"][0:5] == "N2001":
                patch_level(below_50_range, i)
            elif content[i]["Key"][0:5] == "N2015":
                patch_level(chance_3_range, i)
            else:
                patch_level(chance_6_range, i)
        i += 1
    #EndgameBosses
    i = 157
    while i <= 177:
        if resist and content[i]["Value"]["ZAN"] != 100.0:
            rand_stat(i)
        if level:
            if content[i]["Key"] == "N1011":
                patch_level(below_50_range, i)
            elif content[i]["Key"] == "N1004":
                patch_level(chance_4_range, i)
            elif content[i]["Key"] == "N1008" or content[i]["Key"] == "N1011_STRONG":
                patch_level(chance_3_range, i)
            else:
                patch_level(chance_2_range, i)
        i += 1
    #Breeder
    if resist and content[i]["Value"]["ZAN"] != 100.0:
        rand_stat(185)
        rand_stat(186)
    if level:
        patch_level(chance_6_range, 185)
        patch_level(chance_6_range, 186)

def patch_level(array, position):
    if content[position]["Key"] == "N3001_Armor":
        content[position]["Value"]["DefaultEnemyLevel"] = content[38]["Value"]["DefaultEnemyLevel"]
        stat_scale(position)
    elif content[position]["Key"] == "N3098_Guard":
        content[position]["Value"]["DefaultEnemyLevel"] = content[position-2]["Value"]["DefaultEnemyLevel"]
        stat_scale(position)
    elif content[position]["Key"][0:5] == "N1013" or content[position]["Key"] == "N1009_Bael":
        content[position]["Value"]["DefaultEnemyLevel"] = abs(content[159]["Value"]["DefaultEnemyLevel"] - 100)
        stat_scale(position)
        if content[position]["Key"] == "N1013_Dominique":
            create_log(position)
    elif content[position]["Key"][0:5] == content[position-1]["Key"][0:5] and content[position]["Key"][0:5] != "N1011" or content[position]["Key"] == "JuckPod" or content[position]["Key"][0:5] == "N3125":
        content[position]["Value"]["DefaultEnemyLevel"] = content[position-1]["Value"]["DefaultEnemyLevel"]
        stat_scale(position)
    elif content[position]["Key"] != "P1003" and content[position]["Key"] != "N1011_PL" and content[position]["Key"] != "N3049" and content[position]["Key"] != "N3050" and content[position]["Key"] != "N3068":
        content[position]["Value"]["DefaultEnemyLevel"] = random.choice(array)
        stat_scale(position)
        create_log(position)
    
    content[position]["Value"]["HardEnemyLevel"] = content[position]["Value"]["DefaultEnemyLevel"]
    content[position]["Value"]["NightmareEnemyLevel"] = content[position]["Value"]["DefaultEnemyLevel"]
    content[position]["Value"]["BloodlessModeDefaultEnemyLevel"] = content[position]["Value"]["DefaultEnemyLevel"]
    content[position]["Value"]["BloodlessModeHardEnemyLevel"] = content[position]["Value"]["DefaultEnemyLevel"]
    content[position]["Value"]["BloodlessModeNightmareEnemyLevel"] = content[position]["Value"]["DefaultEnemyLevel"]

def stat_scale(position):
    for i in second_stat:
        stat_num = content[position]["Value"][i]
        if content[position]["Value"]["DefaultEnemyLevel"] > content[position]["Value"]["HardEnemyLevel"]:
            stat_num += 25.0
        if content[position]["Value"]["DefaultEnemyLevel"] > (content[position]["Value"]["HardEnemyLevel"] + ((99 - content[position]["Value"]["HardEnemyLevel"]) / 2)):
            stat_num += 25.0
        if stat_num > 100.0:
            stat_num = 100.0
        content[position]["Value"][i] = stat_num

def rand_stat(position):
    if content[position]["Key"] == "N3015_HEAD" or content[position]["Key"] == "N1001_HEAD" or content[position]["Key"] == "N2001_HEAD":
        for i in stat:
            if content[position-1]["Value"][i] < -50:
                content[position]["Value"][i] = -100
            else:
                content[position]["Value"][i] = content[position-1]["Value"][i]-50
    elif content[position]["Key"] == "N3001_Armor":
        for i in stat:
            content[position]["Value"][i] = content[38]["Value"][i]
    elif content[position]["Key"] == "N1001_Tentacle":
        for i in stat:
            content[position]["Value"][i] = content[position-2]["Value"][i]
    elif content[position]["Key"] == "N2001_ARMOR":
        for i in stat:
            if content[position-2]["Value"][i] > 50:
                    content[position]["Value"][i] = 100
            else:
                content[position]["Value"][i] = content[position-2]["Value"][i]+50
    elif content[position]["Key"][0:5] == "N1013" and content[position]["Key"] != "N1013_Bael" or content[position]["Key"] == "N1009_Bael":
        for i in stat:
            content[position]["Value"][i] = content[168]["Value"][i]
    elif content[position]["Key"][0:5] == content[position-1]["Key"][0:5] and content[position]["Key"][0:5] != "N1011" or content[position]["Key"][0:5] == "N3125":
        for i in stat:
            content[position]["Value"][i] = content[position-1]["Value"][i]
    elif content[position]["Key"] != "P1003" and content[position]["Key"] != "JuckPod" and content[position]["Key"] != "N1011_PL" and content[position]["Key"] != "N3049" and content[position]["Key"] != "N3050" and content[position]["Key"] != "N3068":
        for i in stat:
            content[position]["Value"][i] = random.choice(stat_pool)

def create_log(position):
    log_data = {}
    log_data["Key"] = translation["Value"][content[position]["Key"]]
    log_data["Value"] = {}
    log_data["Value"]["Level"] = content[position]["Value"]["DefaultEnemyLevel"]
    log_data["Value"]["MainStats"] = {}
    log_data["Value"]["MainStats"]["HP"] = int(((content[position]["Value"]["MaxHP99Enemy"] - content[position]["Value"]["MaxHP"])/98)*(content[position]["Value"]["DefaultEnemyLevel"]-1) + content[position]["Value"]["MaxHP"])
    log_data["Value"]["MainStats"]["STR"] = int(((content[position]["Value"]["STR99Enemy"] - content[position]["Value"]["STR"])/98)*(content[position]["Value"]["DefaultEnemyLevel"]-1) + content[position]["Value"]["STR"])
    log_data["Value"]["MainStats"]["INT"] = int(((content[position]["Value"]["INT99Enemy"] - content[position]["Value"]["INT"])/98)*(content[position]["Value"]["DefaultEnemyLevel"]-1) + content[position]["Value"]["INT"])
    log_data["Value"]["MainStats"]["CON"] = int(((content[position]["Value"]["CON99Enemy"] - content[position]["Value"]["CON"])/98)*(content[position]["Value"]["DefaultEnemyLevel"]-1) + content[position]["Value"]["CON"])
    log_data["Value"]["MainStats"]["MND"] = int(((content[position]["Value"]["MND99Enemy"] - content[position]["Value"]["MND"])/98)*(content[position]["Value"]["DefaultEnemyLevel"]-1) + content[position]["Value"]["MND"])
    log_data["Value"]["MainStats"]["LUC"] = int(((content[position]["Value"]["LUC99Enemy"] - content[position]["Value"]["LUC"])/98)*(content[position]["Value"]["DefaultEnemyLevel"]-1) + content[position]["Value"]["LUC"])
    log_data["Value"]["MainStats"]["EXP"] = int(((content[position]["Value"]["Experience99Enemy"] - content[position]["Value"]["Experience"])/98)*(content[position]["Value"]["DefaultEnemyLevel"]-1) + content[position]["Value"]["Experience"])
    log_data["Value"]["MainStats"]["AP"] = int(((content[position]["Value"]["ArtsExperience99Enemy"] - content[position]["Value"]["ArtsExperience"])/98)*(content[position]["Value"]["DefaultEnemyLevel"]-1) + content[position]["Value"]["ArtsExperience"])
    log_data["Value"]["Resistances"] = {}
    for i in stat:
        log_data["Value"]["Resistances"][i] = int(content[position]["Value"][i])
    for i in second_stat:
        log_data["Value"]["Resistances"][i] = int(content[position]["Value"][i])
    log.append(log_data)

def write_chara(patched):
    if patched:
        with open("Serializer\\PB_DT_CharacterParameterMaster.json", "w", encoding="utf-8") as file_writer:
            file_writer.write(json.dumps(content, indent=2))
        root = os.getcwd()
        os.chdir("Serializer")
        os.system("cmd /c UAsset2Json.exe -tobin PB_DT_CharacterParameterMaster.json")
        os.chdir(root)
        shutil.move("Serializer\\PB_DT_CharacterParameterMaster.bin", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\Enemy\\PB_DT_CharacterParameterMaster.uasset")
        os.remove("Serializer\\PB_DT_CharacterParameterMaster.json")
    else:
        shutil.copyfile("Serializer\\PB_DT_CharacterParameterMaster.uasset", "UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\Enemy\\PB_DT_CharacterParameterMaster.uasset")

def reset_chara():
    if os.path.isfile("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\Enemy\\PB_DT_CharacterParameterMaster.uasset"):
        os.remove("UnrealPak\\Mod\\BloodstainedRotN\\Content\\Core\\DataTable\\Enemy\\PB_DT_CharacterParameterMaster.uasset")

def write_chara_log():
    with open("SpoilerLog\\Enemy.json", "w", encoding="utf-8") as file_writer:
        file_writer.write(json.dumps(log, indent=2))

def reset_chara_log():
    if os.path.isfile("SpoilerLog\\Enemy.json"):
        os.remove("SpoilerLog\\Enemy.json")