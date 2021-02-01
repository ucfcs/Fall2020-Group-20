import json
from bs4 import BeautifulSoup
import requests
import pandas as pd




if __name__ == '__main__':
    
    filename = "C:/Users/iplea/Desktop/mapinfo.csv"
    f = open(filename, "w")
    headers = "map-name, #-of-Games, TvZ-total, TvZ-T, TvZ-Z, TvZ%, PvZ-total, PvZ-Z, PvZ-P, PvZ%, PvT-total, PvT-P, PvT-T, PvT%, TvT, ZvZ, PvP\n"
    f.write(headers)
    URList = []
    URList.append('https://liquipedia.net/starcraft2/Eternal_Empire_LE')
    URList.append('https://liquipedia.net/starcraft2/Ever_Dream_LE')
    URList.append('https://liquipedia.net/starcraft2/Deathaura_LE')
    URList.append('https://liquipedia.net/starcraft2/Ice_and_Chrome_LE')
    URList.append('https://liquipedia.net/starcraft2/Pillars_of_Gold_LE')

    for URL in URList:
    #URL = 'https://liquipedia.net/starcraft2/Eternal_Empire_LE'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        mdata = ""
    
        results = soup.findAll("tr", {"class":"stats-map-row"})
        for result in results:
            maps = result.findAll("td")
            for header in maps:           
                mdata = mdata + header.text + ", "
    
            f.write(mdata)
            f.write("\n")
    
    f.close()


        
