from django.db import transaction
from rest_framework import serializers
from ..models.user import CustomUser
from ..services.UserService import UserService
from programs.models.program import Program


class UserProgramField(serializers.RelatedField):
    def to_representation(self, value):
        from programs.serializers.ProgramSerializer import ProgramSerializer
        return ProgramSerializer(value).data


class UserSerializer(serializers.ModelSerializer):
    program_set = UserProgramField(many=True, queryset=Program.objects.all())

    class Meta:
        model = CustomUser
        fields = ['id',
                  'author_name',
                  'full_name',
                  'id_type',
                  'id_number',
                  'ist_student_options',
                  'ist_student_number',
                  'phone',
                  'state',
                  'entrance_date',
                  'department',
                  'role',
                  'notes',
                  'date_joined',
                  'exit_date',
                  'is_active',
                  'is_registered',
                  'program_set']

    @transaction.atomic
    def create(self, validated_data):
        programs_data = validated_data.pop('program_set')
        created_user = UserService().create_user(**validated_data)
        for program in programs_data:
            program_authors = list(program.authors.all())
            program_authors.append(created_user)
            program.authors.set(program_authors)
        return created_user

    @transaction.atomic
    def update(self, instance, validated_data):
        if 'program_set' in validated_data:
            new_programs_data = validated_data.pop('program_set')
            previous_programs_data = instance.program_set.all()
            for program in new_programs_data:
                if program not in previous_programs_data:
                    program_authors = list(program.authors.all())
                    program_authors.append(instance)
                    program.authors.set(program_authors)

            for program in previous_programs_data:
                if program not in new_programs_data:
                    program_authors = list(program.authors.all())
                    program_authors.remove(instance)
                    program.authors.set(program_authors)

        return UserService().update_user(instance, **validated_data)
