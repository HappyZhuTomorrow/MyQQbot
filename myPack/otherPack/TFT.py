from os import linesep
import requests
import json

def spiderTFT():
        head = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
        }
        r = requests.get("https://game.gtimg.cn/images/lol/act/tftzlkauto/json/lineupJson/s6/6/lineup_detail_total.json?v=9115406",headers=head)
        

        
        
        heroList = [[]for j in range(28)]
        lines = open("./File/英雄对照.txt",encoding='utf-8').readlines()
        flag = 0
        for i in range(28):
            
            lineup_list = json.loads(r.content.decode())['lineup_list'][i]['detail']
            hero_location = json.loads(lineup_list,strict=False)["hero_location"]
            for hero in hero_location:
                if i==9:
                    if flag != 0:
                        for line in lines:
                            lineSplit = line.split()
                            if hero["hero_id"] == lineSplit[0]:
                                heroList[i].append(lineSplit[1].strip('\n'))
                    else:
                        flag = flag+1
                        continue
                else:
                    for line in lines:
                        lineSplit = line.split()
                        if hero["hero_id"] == lineSplit[0]:
                            heroList[i].append(lineSplit[1].strip('\n'))

        return heroList       
                    
        print(heroList)
            
if __name__ == '__main__':
    print(spiderTFT())
