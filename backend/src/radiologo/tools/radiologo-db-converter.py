"""
This utility converts the DB currently in Production, related with the 2nd version of Radiólogo, to a DB for the new
improved 3rd version.
There are 3 main instances we need to convert:

CustomUser -> CustomUser
Programas -> Programs
Days -> Slots

HOW TO USE
create the Django DB with `pipenv run python manage.py migrate`
put the old DB file in the src directory and rename it to production.sqlite3
cd into the src directory, and run:
`python3 radiologo/tools/radiologo-db-converter.py`
"""
import sqlite3


class DBConverter:
    def __init__(self, old_db_path: str, new_db_path: str):
        self.old_db_path = old_db_path
        self.new_db_path = new_db_path

    def do_conversion(self):
        old_db = sqlite3.connect(self.old_db_path)
        new_db = sqlite3.connect(self.new_db_path)
        self.convert_users(old_db, new_db)
        self.convert_programs(old_db, new_db)
        self.convert_program_authors(old_db, new_db)
        self.convert_slots(old_db, new_db)

    def convert_users(self, old_db, new_db):
        old_cur = old_db.cursor()
        old_cur.execute("SELECT * FROM membros_customuser")
        old_users = old_cur.fetchall()
        old_users_list = []
        old_fields = [field[0] for field in old_cur.description]
        for row in old_users:
            user = {}
            for i in range(len(row)):
                user[old_fields[i]] = row[i]
            if user["department"] is None:
                user["department"] = "NA"
            if user["role"] is None:
                user["role"] = "NA"
            old_users_list.append(user)

        new_cur = new_db.cursor()
        new_cur.execute("SELECT * FROM users_customuser")
        new_fields = [field[0] for field in new_cur.description]
        query = "INSERT INTO users_customuser({}) VALUES(?{})".format(",".join(new_fields),
                                                                      ",?" * (len(new_fields) - 1))
        for user in old_users_list:
            new_user = (
                user["id"], user["password"], user["last_login"], user["is_superuser"], user["email"], user["is_staff"],
                user["author_name"], user["full_name"], user["tipo_id"], user["num_id"], user["aluno_ist"],
                user["numero_aluno_ist"], user["phone"], user["state"], user["entrance_date"], user["department"],
                user["role"], user["notes"], user["date_joined"], user["exit_date"], user["is_active"], True, "")
            new_cur.execute(query, new_user)
        new_db.commit()

    def convert_programs(self, old_db, new_db):
        old_cur = old_db.cursor()
        old_cur.execute("SELECT * FROM gerir_programa")
        old_programs = old_cur.fetchall()
        old_programs_list = []
        old_fields = [field[0] for field in old_cur.description]
        print(old_fields)
        for row in old_programs:
            program = {}
            for i in range(len(row)):
                program[old_fields[i]] = row[i]
            old_programs_list.append(program)

        new_cur = new_db.cursor()
        new_cur.execute("SELECT * FROM programs_program")
        new_fields = [field[0] for field in new_cur.description]
        query = "INSERT INTO programs_program({}) VALUES(?{})".format(",".join(new_fields),
                                                                      ",?" * (len(new_fields) - 1))
        print(new_fields)
        for program in old_programs_list:
            new_program = (
                program["id"], program["name"], program["description"], program["duracao_maxima"],
                program["primeira_emissao"], program["vem_normalizado"], program["ignorarAjuste"],
                program["externo"], program["estado"], False, ""
            )
            new_cur.execute(query, new_program)
        new_db.commit()

    def convert_program_authors(self, old_db, new_db):  # field names in old db are equal to the new db
        old_cur = old_db.cursor()
        old_cur.execute("SELECT * FROM gerir_programa_authors")
        old_programs = old_cur.fetchall()
        old_fields = [field[0] for field in old_cur.description]
        print(old_fields)
        new_cur = new_db.cursor()
        for row in old_programs:
            query = "INSERT INTO programs_program_authors(id, program_id, customuser_id) VALUES(?,?,?)"
            new_cur.execute(query, row)
        new_db.commit()

    def convert_slots(self, old_db, new_db):
        old_cur = old_db.cursor()
        old_cur.execute("SELECT * FROM gerir_days")
        old_slots = old_cur.fetchall()
        old_slots_list = []
        old_fields = [field[0] for field in old_cur.description]
        print(old_fields)
        for row in old_slots:
            slot = {}
            for i in range(len(row)):
                slot[old_fields[i]] = row[i]
            old_slots_list.append(slot)

        new_cur = new_db.cursor()
        new_cur.execute("SELECT * FROM programs_slot")
        new_fields = [field[0] for field in new_cur.description]
        query = "INSERT INTO programs_slot({}) VALUES(?{})".format(",".join(new_fields),
                                                                   ",?" * (len(new_fields) - 1))
        print(new_fields)
        for slot in old_slots_list:
            new_slot = (slot["id"], int(slot["day"])+1, slot["time"], slot["programa_associado_id"], False)
            new_cur.execute(query, new_slot)
        new_db.commit()


def main():
    converter = DBConverter("production.sqlite3", "db.sqlite3")
    converter.do_conversion()


main()
