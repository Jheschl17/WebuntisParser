from datetime import date


class TimedTeacherLocation:

    def __init__(self, teacher: str, location: str, date: date, lesson: int):
        self.teacher = teacher
        self.location = location
        self.date = date
        self.lesson = lesson

    teacher: str
    location: str
    date: date
    lesson: int

    def __str__(self):
        return f'{{{self.teacher}, {self.location}, {self.date}, {self.lesson}}}'
