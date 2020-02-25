import math

from bs4 import BeautifulSoup
from bs4 import Tag
from datetime import date, timedelta
import re
import requests

from TimedTeacherLocation import TimedTeacherLocation

FIRST_CLASS_ID: int = 183
LAST_CLASS_ID: int = 200
REQUEST_HEADER: map = {
    'Cookie': 'schoolname="_aHRibGEtZ3JpZXNraXJjaGVu";'
}


def extract_teachers(lesson_outer: Tag) -> [str]:
    if len(list(lesson_outer.children)) == 0:
        return []
    teachers: str = list(lesson_outer.table.tr.td.table.children)[2].text
    return re.split(',\\s*', teachers)


def extract_location(lesson_outer: Tag) -> str:
    if len(list(lesson_outer)) == 0:
        return ''
    return list(lesson_outer.table.tr.td.table.children)[4].text


def extract_timed_teacher_locations(soup: BeautifulSoup, mondayte: date) -> [TimedTeacherLocation]:
    timed_teacher_locations: [TimedTeacherLocation] = []
    table = soup.find(id='timetable').table
    rows = table.children
    next(rows)
    for idx_row, row in enumerate(rows):
        if row == '\n':
            continue
        day_of_week: float = 0
        for idx_lesson, lesson in enumerate(row):
            if idx_lesson == 0:
                continue
            if 'ttcell' in lesson.attrs['class']:
                teachers: [str] = extract_teachers(lesson)
                location: str = extract_location(lesson)
                rowspan: int = int(lesson.attrs['rowspan']) if 'rowspan' in lesson.attrs else 1
                for teacher in teachers:
                    for i in range(rowspan):
                        timed_teacher_locations.append(
                            TimedTeacherLocation(
                                teacher=teacher,
                                location=location,
                                lesson=math.ceil(idx_row / 2) + i,
                                dt=mondayte + timedelta(days=day_of_week)
                            )
                        )
            if 'br' in lesson.attrs['class']:
                day_of_week += 1
    return timed_teacher_locations


def download_soups(mondayte: date) -> [BeautifulSoup]:
    ret: [BeautifulSoup] = []
    for i in range(FIRST_CLASS_ID, LAST_CLASS_ID + 1):
        response = requests.get(
            construct_request_url(mondayte, i),
            headers=REQUEST_HEADER
        )
        ret.append(BeautifulSoup(response.content, "html.parser"))
    return ret


def construct_request_url(mondayte: date, class_id: int) -> str:
    date_formatted: str = mondayte.strftime('%Y%m%d')
    return f'https://arche.webuntis.com/WebUntis/api/public/printpreview/' \
           f'timetable?type=1&id={class_id}&date={date_formatted}&formatId=7'
