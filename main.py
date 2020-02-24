from bs4 import BeautifulSoup

with open('resources/WebUntis-3a-20200224.html') as fp:
    soup = BeautifulSoup(fp, 'html.parser')
    table = soup.find(id='timetable').table.tbody
    print(table)
