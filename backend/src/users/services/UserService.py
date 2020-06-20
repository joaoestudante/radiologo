from ..managers import CustomUserManager
from ..models import CustomUser


class UserService:
    def __init__(self):
        self.user_manager = CustomUserManager()

    def create_user(self, **data):
        if data.get('is_superuser', False):
            u = CustomUser.objects.create_superuser(**data)
        else:
            u = CustomUser.objects.create_user(**data)
        u.save()
        return u

    def create_superuser(self, **data):
        u = self.create_user(**data, is_superuser=True)
        u.save()
        return u

    def update_user(self, user, **new_data):
        user.author_name = new_data.get('author_name', user.author_name)
        user.full_name = new_data.get('full_name', user.full_name)
        user.id_type = new_data.get('id_type', user.id_type)
        user.id_number = new_data.get('id_number', user.id_number)
        user.ist_student_options = new_data.get('ist_student_options', user.ist_student_options)
        user.ist_student_number = new_data.get('ist_student_number', user.ist_student_number)
        user.phone = new_data.get('phone', user.phone)
        user.state = new_data.get('state', user.state)
        user.entrance_date = new_data.get('entrance_date', user.entrance_date)
        user.department = new_data.get('department', user.department)
        user.role = new_data.get('role', user.role)
        user.notes = new_data.get('notes', user.notes)
        user.date_joined = new_data.get('date_joined', user.date_joined)
        user.exit_date = new_data.get('exit_date', user.exit_date)
        user.is_active = new_data.get('is_active', user.is_active)
        user.save()
        return user

