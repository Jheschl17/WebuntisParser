from datetime import date


class TimedTeacherLocation:

    teacher: str
    location: str
    date: date
    lesson: int

    def __init__(self, teacher: str, location: str, dt: date, lesson: int):
        self.teacher = teacher
        self.location = location
        self.date = dt
        self.lesson = lesson

    def __str__(self):
        return f'{{{self.teacher}, {self.location}, {self.date}, {self.lesson}}}'
