from bs4 import BeautifulSoup
from bs4 import Tag
from datetime import date, timedelta
import re
import requests
import numpy as np

from src.TimedTeacherLocation import TimedTeacherLocation

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
    marks: [[bool]] = np.zeros((calc_total_table_width(table), 10), dtype=bool)  # [day][lesson]
    rows = filter(lambda it: it != '\n', table.children)
    next(rows)
    for row_num, row in enumerate(rows):
        lessons = filter(lambda it: 'ttcell' in it.attrs['class'], row.children)
        for lesson_num, lesson in enumerate(lessons):
            for teacher in extract_teachers(lesson):
                for i in range(int(lesson.attrs['rowspan']) if 'rowspan' in lesson.attrs else 1):
                    timed_teacher_locations.append(TimedTeacherLocation(
                        teacher=teacher,
                        location=extract_location(lesson),
                        lesson=row_num + i + 1,
                        dt=determine_current_date(marks, row_num, row, mondayte)
                    ))
            mark(lst=marks,
                 origin_x=row_num,
                 origin_y=lesson_num,
                 down=int(lesson.attrs['rowspan']) if 'rowspan' in lesson.attrs else 1,
                 right=int(lesson.attrs['colspan']) if 'colspan' in lesson.attrs else 1)
    return timed_teacher_locations


def mark(lst: [[bool]], origin_x: int, origin_y: int, down: int, right: int):
    """
    marks elements in a rectangle starting from origin, downwards for down elements
    and rightwards for right elements.
    :param lst: the list in which elements should be marked
    :param origin_x: the x coordinate from where marking should start
    :param origin_y: the y coordinate from where marking should start
    :param down: how far down elements should be marked
    :param right: how far right elements should be marked
    :return:
    """
    for y in range(origin_y, down):
        for x in range(origin_x, right):
            lst[y][x] = True


def determine_current_date(marks: [[bool]], row: int, sample_row: Tag, mondayte: date) -> date:  # ????
    mark_row = marks[row]
    elem = list(mark_row).index(False)
    day_counter = 0
    for i in range(0, elem):
        if 'br' in list(sample_row.children)[i].attrs['class']:
            day_counter += 1
    return mondayte + timedelta(days=day_counter)


def calc_total_table_width(table: Tag) -> int:
    width_counter: int = 0
    for lesson in list(list(table.children)[2].children)[1:]:
        lesson_duration: int = int(lesson.attrs['colspan']) if 'colspan' in lesson.attrs else 1
        width_counter += lesson_duration
    return width_counter


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
