import json
from bs4 import BeautifulSoup
import requests


def GetStuff(results, verbose_level=0):
    races = {}

    for h2 in results.find_all('h2')[1:4]:
        races[h2.text] = {}

        if verbose_level > 0:
            print(h2.text)

        h3s = h2.fetchNextSiblings('h3')[:3]
        for i, h3 in enumerate(h3s):
            races[h2.text][h3.text] = {}

            a = len(h3.fetchNextSiblings('h4'))
            b = len(h3s[i+1].fetchNextSiblings('h4')) if i < len(h3s)-1 else 0
            c = a - b

            if verbose_level > 1:
                print('\t', h3.text)

            if c == 0:
                table = h3.fetchNextSiblings('table')[0]
                races[h2.text][h3.text]['Units'] = [tr.find_all('td')[1].a.text for tr in table.tbody.find_all('tr')[1:]]

                if verbose_level > 2:
                    print('\t\t', 'Units')
                    for d in races[h2.text][h3.text]['Units']:
                        print('\t\t\t', d)
            else:
                for h4 in h3.fetchNextSiblings('h4')[:a-b]:
                    table = h4.fetchNextSiblings('table')[0]

                    races[h2.text][h3.text][h4.text] = [tr.find_all(
                        'td')[1].a.text for tr in table.tbody.find_all('tr')[1:]]

                    if verbose_level > 2:
                        print('\t\t', h4.text)
                        for d in races[h2.text][h3.text][h4.text]:
                            print('\t\t\t', d)
    
    return races


if __name__ == '__main__':
    URL = 'https://starcraft.fandom.com/wiki/List_of_StarCraft_II_units'
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(class_='mw-parser-output')

    # To get all output change verbose_level >= 3
    stuff = GetStuff(results, verbose_level=2)

    # Set to True to save as whatever file_ value
    if False:
        file_ = './units_dump.json'
        with open(file_, 'w') as f:
            json.dump(stuff, f)
        print('Saved as', file_)
