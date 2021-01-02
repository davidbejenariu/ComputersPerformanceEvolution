from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import requests

def getPerformance(month, year):
    f = open('perfValues.txt', 'a')
    link = 'https://top500.org/lists/top500/' + str(year) + '/' + month + '/'
    html_code = requests.get(link).text
    soup = BeautifulSoup(html_code, 'lxml')
    table_list = soup.find_all('td')
    #extragem valorile pentru primele 3 calculatoare
    value1 = float(table_list[3].text.replace(',',''))
    value2 = float(table_list[9].text.replace(',',''))
    value3 = float(table_list[15].text.replace(',',''))
    #inainte de 2005 valorile erau masurate in GFlop/s
    if int(year) <= 2004:
        value1 = value1 / 1000
        value2 = value2 / 1000
        value3 = value3 / 1000
    #adaugam in fisier valorile impreuna cu periaoda de timp
    f.write('Month:' + month + ',' + 'Year:' + str(year) + ',' + str(value1) + ',' + str(value2) + ',' + str(value3) + '\n')
    f.close()

# in prima faza, extragem valorile de pe site si le punem intr-un fisier

year = 1993
while True:
    f = open('perfValues.txt', 'r')
    reader = f.read()
    f.close()
    # verificam daca pentru luna iunie a anului avem in fisier valorile
    string = 'Month:' + '06' + ',Year:' + str(year)
    if string not in reader:
        #verificam daca exista lista pe site
        link = 'https://top500.org/lists/top500/' + str(year) + '/' + '06' + '/'
        if requests.get(link).status_code == 200:
            getPerformance('06', str(year))
        else:
            break
    #verificam pentru noiembrie
    string = 'Month:' + '11' + ',Year:' + str(year)
    if string not in reader:
        link = 'https://top500.org/lists/top500/' + str(year) + '/' + str(11) + '/'
        if requests.get(link).status_code == 200:
            getPerformance('11', str(year))
        else:
            break
    year += 1

#generam graficul si calculam media
x = []
y = []
f = open('perfValues.txt', 'r')
reader = f.read().split('\n')
for str in reader:
    if len(str) > 1:
        list = str.split(',')
        if list[0][6:7] == '0':
            month = 'Jun '
        else:
            month = 'Nov '
        year = list[1][5:9]
        value1 = float(list[2])
        value2 = float(list[3])
        value3= float(list[4])
        x.append(month + year)
        y.append( (value1 + value2 + value3) / 3)

#graficul cu valorile all-time
plt.plot(x,y)
plt.xticks(x, x, rotation='vertical')
plt.title('Evoluția perfomanței super-calculatoarelor')
plt.xlabel('Luna, An')
plt.ylabel('Valoarea Rmax medie a primelor 3 calculatoare (TFlop/s)')
plt.show()
#graficul cu valorile pana in 2001
plt.plot(x,y)
plt.xticks(x, x, rotation='vertical')
plt.title('Evoluția perfomanței super-calculatoarelor până în anul 2001')
plt.xlabel('Luna, An')
plt.ylabel('Valoarea Rmax medie a primelor 3 calculatoare (TFlop/s)')
plt.axis(['Jun 1993','Nov 2001',0, 6])
plt.show()

# evolutia medie calculata sub forma unei medii aritmetice a raporturilor de putere intre 2 ani consecutivi

diff = 0
for i in range(0, len(y)-3, 2):
    diff += (y[i+2] + y[i+3]) / (y[i] + y[i+1])
diff = diff / (len(y) / 2) * 100
diff = round(diff,2)
print('Progresul mediu realizat pe an: ', diff, '%', sep = '')

