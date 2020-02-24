from datetime import date
from bs4 import BeautifulSoup

import TimedTeacherLocation
from WebUntisParserUtil import *


timedTeacherLocations = [TimedTeacherLocation]

mondayte: date = date(2020, 2, 24)  # date of monday TODO: generate automatically
with open('resources/WebUntis-3a-20200224.html') as fp:
    soup = BeautifulSoup(fp, 'html.parser')
    table = soup.find(id='timetable').table.tbody
    rows = table.children
    next(rows)
    for idx_row, row in enumerate(rows):
        if row == '\n':
            continue
        for idx_lesson, lesson in enumerate(row):
            if idx_lesson == 0:
                continue
            day_of_week: float = 0
            teachers: [str] = extract_teachers(lesson)
            location: str = extract_location(lesson)
            for teacher in teachers:
                timedTeacherLocations.append(
                    TimedTeacherLocation(teacher=teacher, location=location, lesson=idx_lesson, date=mondayte + day_of_week)
                )
