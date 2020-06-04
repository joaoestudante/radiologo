from ..models import Program

class ProgramService:
    def __init__(self):
        pass

    def create_program(self, name, description, authors, max_duration, **extra_fields):
        p = Program(name=name, description=description, max_duration=max_duration, **extra_fields)
        p.save()
        p.authors.set(authors)
        return p