import requests
from bs4 import BeautifulSoup
from urllib import parse
import re
def getTop(num):
    TopList = [[]for i in range(20)]
    TopList_fin = []
    j = 0
    r = requests.get("https://www.scoregg.com/big-data/ranking")
    soup = BeautifulSoup(r.text,'lxml')
    data_first = soup.findAll(attrs={'class':'first'}) #排名
    data_name = soup.findAll(attrs={'class':'name'}) #游戏id
    data_segment = soup.findAll(attrs={'class':'tier'}) #rank分数
    # data_win = soup.findAll(attrs={'class':'item'}) #胜率
    #__layout > div > div.big-data-nuxt > div.page-main > div:nth-child(1) > div > div.table-container > div.tables > table > tbody > tr:nth-child(1) > td.team > a:nth-child(2) > i
    # data_team = soup.select("__layout > div > div.big-data-nuxt > div.page-main > div > div > div.table-container > div.tables > table > tbody > tr > td.team  ")
    # print(data_team)
    for d in data_first:
        
        TopList[j].append(str(d).replace('<span class="first" data-v-0cd5c67f=""><i data-v-0cd5c67f="">','').replace('</i>','').replace('</span>',''))
        j = j+1

    j = 0
    for d in data_name:
        TopList[j].append(str(d).replace('<div class="name" data-v-0cd5c67f=""><p data-v-0cd5c67f="">','').replace('</p>','').replace('</div>',''))
        j = j+1

    j = 0
    for d in data_segment:
        TopList[j].append(str(d).replace('<div class="tier" data-v-0cd5c67f=""><img class="tier-icon" data-v-0cd5c67f="" src="https://img.scoregg.com/images/lol/tier/challenger.png"/> <p data-v-0cd5c67f="">','').replace('</p>','').replace('</div>',''))
        j = j+1

    for i in range(num):
        TopList_fin.append(TopList[i])
    return TopList_fin


def getRank(QQ_id):
    LOLnames = open('./File/lol名字.txt',encoding='utf-8').read().splitlines()
    for name in LOLnames:
        nameSplit = name.split(' ')
        if QQ_id == int(nameSplit[0]):
            lolname = nameSplit[1]
            break
    
    b = parse.quote(lolname)
    rankList = [[]for i in range(5)]
    url_temp = 'https://www.lolhelper.cn/rank_lcu.php?gameid={}&server=17'
    url = url_temp.format(b)
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'lxml')
    data = soup.findAll(attrs={'class':'main_tit'})
    data2 = soup.findAll(attrs={'class':'main_txt'})
    strData = str(data).replace('[<div class="main_tit">','').replace('</div>','').replace('<div class="main_tit">','').replace(']','')
    strData2 = str(data2).replace('[<div class="main_txt">','').replace('</div>','').replace('<div class="main_txt">','').replace(']','')
    strDataList = strData.split(',')
    strData2List = strData2.split(',')
    for i in range(5):
        rankList[i].append(str(strDataList[i]).strip())
        rankList[i].append(str(strData2List[i]).strip())
    rankList[0],rankList[3] = rankList[3],rankList[0]
    return rankList
    print(rankList)



if __name__ == '__main__':
    # print(getTop(2))
    print(getRank(1639253554))
