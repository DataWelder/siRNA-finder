import json
import re
from colorama import Fore, init, Style
init(convert=True)

confirmed_aag = []
atg_positions = []
aag_positions = []
data = ''

def repetitions(str):
    x0 = x1 = x2 = x3 = None
    x0 = re.search("AAAA", str)
    x1 = re.search("TTTT", str)
    x2 = re.search("CCCC", str)
    x3 = re.search("GGGG", str)
    if x0 == None and x1 == None and x2 == None and x3 == None:
        return True
    else:
        return False
     

def checkAAG(position, data):
    warunki = True
    aag = data[position : position+25]
    # print("Check("+ str(position) + "): " + aag)
    if aag[12] == 'G':
        warunki = False
        # print("Jest G na 13 pozycji")
    if aag[9] != 'A' and aag[9] != 'T':
        warunki = False
        # print("brak A lub T na 10 pozycji")
                
    if warunki == True:
        aag_end = 0
                    
        for match in re.finditer('AA', aag):
            if match.end() >= 19 and match.end() <= 25:
                aag_end = match.end()
                break
                    
        for match in re.finditer('TT', aag):
            if match.end() >= 19 and match.end() <= 25 and match.end() > aag_end:
                aag_end = match.end()
                break
                    
        if aag_end > 0:
            aag = aag[0 : aag_end]
            if repetitions(aag):
                print( aag + " - " + str(aag_end))
                conf = {'start': position, 'end': position+aag_end}
                confirmed_aag.append(conf)
                return position + aag_end
            else:
                # print('4 takie same nukleotydy po sobie')
                return position
        else:
            # print("brak odpowiedniego zakonczenia")
            return position
    else:
        return position

def findNearestAAG(position, maxrange):
    while position <= maxrange:
        if position in aag_positions:
            return position
        if position in atg_positions:
            return False
        position += 1
    return False

def findNearestATG(position, maxrange):
    while position <= maxrange:
        if position in atg_positions:
            return position
        position += 1
    return False

def satefyPosition(position):
    pos = position
    x = 1
    while x <= 75:
        pos += 1
        if pos in atg_positions:
            x = 1
            continue
        if pos + 1 in atg_positions:
            x = 1
            continue
        if pos + 2 in atg_positions:
            x = 1
            continue
        x += 1
    return pos

def findAAG(wartownik, maxlen):
    while wartownik < maxlen:
        # print(wartownik)
        pos = findNearestAAG(wartownik, maxlen)
        if pos == False:
            pos = findNearestATG(wartownik, maxlen)
            pos = satefyPosition(pos)
            wartownik = pos
            continue
        else:    
            pos = checkAAG(pos, data)
            wartownik = pos
        wartownik = wartownik + 1

with open("config.json", "r") as read_file:
    config = json.load(read_file)
with open('data.txt', 'r') as file:
    data = file.read().replace('\n', '')


len_data = len(data)



for match in re.finditer('ATG', data):
    atg_positions.append(match.end())

for match in re.finditer('AAG', data):
    aag_positions.append(match.start())

wartownik = 0
# checkAAG(2054, data)
findAAG(wartownik, len_data)
# pos = satefyPosition(500)
# print(pos)


print(confirmed_aag)
print(atg_positions)
print(aag_positions)
# print(Fore.LIGHTGREEN_EX + 'test czerwony' + Style.RESET_ALL )
