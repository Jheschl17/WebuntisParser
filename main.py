import math
from datetime import date
from datetime import timedelta
from bs4 import BeautifulSoup

from TimedTeacherLocation import TimedTeacherLocation
from WebUntisParserUtil import *

timedTeacherLocations: [TimedTeacherLocation] = []

mondayte: date = date(2020, 2, 24)  # date of monday TODO: generate automatically
with open('resources/WebUntis-3a-20200224.html') as fp:
    soup = BeautifulSoup(fp, 'html.parser')
    table = soup.find(id='timetable').table.tbody
    rows = table.children
    next(rows)
    for idx_row, row in enumerate(rows):
        if row == '\n':
            continue
        day_of_week: float = 0
        for idx_lesson, lesson in enumerate(row):
            if idx_lesson == 0:
                continue
            teachers: [str] = extract_teachers(lesson)
            location: str = extract_location(lesson)
            for teacher in teachers:
                timedTeacherLocations.append(
                    TimedTeacherLocation(
                        teacher=teacher,
                        location=location,
                        lesson=math.ceil(idx_row / 2),
                        dt=mondayte + timedelta(days=int(day_of_week))
                    )
                )
            if 'bl' in lesson.attrs['class']:
                day_of_week += 0.5
            if 'br' in lesson.attrs['class']:
                day_of_week += 0.5

for timedTeacherLocation in timedTeacherLocations:
    print(timedTeacherLocation)
