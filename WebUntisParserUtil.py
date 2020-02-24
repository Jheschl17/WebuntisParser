import bs4
import re


def extract_teachers(lesson_outer: bs4.Tag) -> [str]:
    if len(list(lesson_outer.children)) == 0:
        return []
    teachers: str = lesson_outer.select('.Z_1_0')[0].text
    return re.split(',\\s*', teachers)


def extract_location(lesson_outer: bs4.Tag) -> str:
    if len(list(lesson_outer)) == 0:
        return ''
    return lesson_outer.select('.Z_2_0')[0].text
