from ..models import Program

class ProgramService:
    def __init__(self):
        pass

    def create_program(self, authors, **extra_fields):
        p = Program(**extra_fields)
        p.save()
        p.authors.set(authors)
        return p