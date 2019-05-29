from bs4 import BeautifulSoup
import pandas as pd
from urllib.request import urlopen
import urllib.error
import collections
import os
import time



Start = time.time()
Path = os.path.dirname(os.path.abspath(__file__))

Base_URL = "http://www.espncricinfo.com/ci/content/player/caps.html?country="
Base_Stats_URL = "http://stats.espncricinfo.com"
Batting_Stats = "?class=2;template=results;type=batting;view=innings"
class_string = ";class=2"

NameList = []
PageLink = []
Complete_list = []
o = 0


#As there are 48 countries that play cricket (According to espncricinfo)
count=48


def Get_Players_NameList(html):
    bs = BeautifulSoup(html, "lxml")

    Player_Content = bs.findAll('a', {'class':"ColumnistSmry",'style':"valign:middle;"})
    for Player_info in Player_Content:
        NameList.append(Player_info.text)
        tobereplaced = Player_info["href"].replace('content','engine')
        PageLink.append(tobereplaced)


def Get_Batting_runs(Player_link):

    Player_URL = Base_Stats_URL + Player_link + Batting_Stats

    try:
        html = urlopen(Player_URL)
    except urllib.error.HTTPError:
        return Get_Batting_runs(Player_link)

    bs = BeautifulSoup(html, "lxml")
    Player_Runs = bs.findAll('tr', {'class': "data1"})
    Player_Date = bs.findAll('td', {'nowrap': "nowrap"})

    for runs in Player_Runs:
        tmp=0
        if runs.td.text.isnumeric():
            Runs.append(runs.td.text)
        else:
            tmp = runs.td.text[0:-1]
            Runs.append(tmp)

    for date in Player_Date:
        if date.b is not None:
            Date.append(date.b.text)


def Get_Year(Date):
    for date in Date:
        Year.append(date[-4:])


def Year_wise_Runs(Year,Runs):
    k=1
    count=collections.Counter(Year)
    frequency_year = count.values()
    for freq in frequency_year:
        sum = 0
        for i in range(freq):
            if Runs[k].isnumeric():
                sum = sum + int(Runs[k])
            k = k+1
        Year_wise_run.append(sum)
    Year = list(dict.fromkeys(Year))
    for i in range(len(Year)):
        years[Year[i]] = Year_wise_run[i]


def Get_Cummalative_Score(years):
    new_list = []
    i=0
    for keys,values in years.items():
        new_list.append(values)
        List = [sum(new_list[0:x + 1]) for x in range(0, len(new_list))]
        cumm_years[keys]=List[i]
        i = i+1

while count>0:
    URL=Base_URL + str(count) + class_string
    print(URL)
    html=urlopen(URL)
    Get_Players_NameList(html)
    count = count-1

print(PageLink)


for playerLink in PageLink:

    Runs = []
    Date = []
    Year = []
    frequency_year = []
    Year_wise_run = []
    years = {}
    cumm_years = {}

    print(NameList[o])

    Get_Batting_runs(playerLink)

    Get_Year(Date)

    Year_wise_Runs(Year, Runs)

    print("The Players Runs in each year : ")
    print(years)

    Get_Cummalative_Score(years)

    print("The Players cummulative runs in each year : ")
    print(cumm_years)

    print("=======================================================================================================================")

    Complete_list.append(years)

    o = o + 1


with open("Names.txt", "w") as output:
    output.write(str(NameList))
with open("Years.txt", "w") as output:
    output.write(str(Complete_list))


end = time.time()

print('Total Time Taken is : ')
print(Start - end)