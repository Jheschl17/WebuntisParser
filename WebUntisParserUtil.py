from bs4 import BeautifulSoup
from bs4 import Tag
from datetime import date
import re
from typing import Final
import requests

FIRST_CLASS_ID: Final = 183
LAST_CLASS_ID: Final = 200


def extract_teachers(lesson_outer: Tag) -> [str]:
    if len(list(lesson_outer.children)) == 0:
        return []
    teachers: str = lesson_outer.select('.Z_1_0')[0].text
    return re.split(',\\s*', teachers)


def extract_location(lesson_outer: Tag) -> str:
    if len(list(lesson_outer)) == 0:
        return ''
    return lesson_outer.select('.Z_2_0')[0].text


def download_soups(mondayte: date) -> [BeautifulSoup]:
    ret: [BeautifulSoup] = []
    for i in range(FIRST_CLASS_ID, LAST_CLASS_ID):
        response = requests.get(construct_request_url(mondayte, i))
        ret.append(BeautifulSoup(response.content, "html.parser"))
    return ret


def construct_request_url(mondayte: date, class_id: int) -> str:
    date_formatted: str = mondayte.strftime(fmt='%Y%m%d')
    return f'https://arche.webuntis.com/WebUntis/api/public/printpreview/' \
           f'timetable?type=1&id={class_id}&date={date_formatted}&formatId=7'
