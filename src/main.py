"""
**All your Lehrerstundenpläne are belong to us**

This program downloads all webuntis timetables for the specified date and generates
teacher timetables accordingly.

To execute run following command while in project directory:
'python3 main.py <date of monday of week to generate timetables for in format dd.mm.yyyy>'

Dependencies:
BeautifulSoup4 (https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
Pystache (https://github.com/defunkt/pystache)
"""

__author__ = "StrauXX"


from src.WebUntisParserUtil import *


timed_teacher_locations: [TimedTeacherLocation] = []

mondayte: date = date(2020, 2, 24)  # date of monday TODO: generate automatically
for soup in download_soups(mondayte):
    timed_teacher_locations.extend(extract_timed_teacher_locations(soup, mondayte))

for ttl in sorted(timed_teacher_locations):
    print(ttl)

"""
data = [
    {
        teacher = '',
        days = [
            {
                date = DATE,
                lessons = [
                    'LOCATION',
                    ...
                ]
            },
            ...
        ]
    },
    ...
]
"""
