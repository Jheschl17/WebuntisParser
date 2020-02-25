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

    def __eq__(self, o: object) -> bool:
        return o.teacher == self.teacher\
               and o.location == self.location\
               and o.date == self.date\
               and o.lesson == self.lesson

    def __lt__(self, other):
        if self.teacher == other.teacher:
            if self.date == other.date:
                return self.lesson < other.lesson
            else:
                return self.date < other.date
        else:
            return self.teacher < other.teacher
