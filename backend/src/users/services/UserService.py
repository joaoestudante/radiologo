from ..managers import CustomUserManager
from ..models import CustomUser
from django.contrib.auth import get_user_model


class UserService:
    def __init__(self):
        self.user_manager = CustomUserManager()

    def create_user(self, email, password, author_name, full_name, id_type, id_number, ist_student_options, phone):
        u = CustomUser(email=email, password=password, author_name=author_name,
                          full_name=full_name, id_type=id_type,
                          id_number=id_number, ist_student_options=ist_student_options, phone=phone)
        u.save()
        return u

    def create_superuser(self, email, password, author_name, full_name, id_type, id_number, ist_student_options, phone):
        u = CustomUser(email=email, password=password, author_name=author_name,
                          full_name=full_name, id_type=id_type,
                          id_number=id_number, ist_student_options=ist_student_options,
                          phone=phone, is_superuser=True)
        u.save()
        return u
