from rest_framework import serializers
from .SlotSerializer import SlotSerializer
from ..models import Program
from ..services.ProgramService import ProgramService
from ..services.SlotService import SlotService
from users.serializers.UserSerializer import UserSerializer
from exceptions.radiologoexception import RadiologoException
from django.contrib.auth import get_user_model


class ProgramSerializer(serializers.ModelSerializer):
    slot_set = SlotSerializer(many=True)
    authors = serializers.PrimaryKeyRelatedField(many=True, queryset=get_user_model().objects.all())

    class Meta:
        model = Program
        fields = ['name', 'description', 'max_duration', 'first_emission_date', 'comes_normalized',
                  'ignore_duration_adjustment', 'is_external', 'state', 'slot_set', 'authors']

    def create(self, validated_data):
        slots_data = validated_data.pop('slot_set')
        authors_data = validated_data.pop('authors')
        created_program = ProgramService().create_program(authors_data, **validated_data)
        created_slots = []
        for slot in slots_data:
            try:
                dict_slot = dict(slot)
                SlotService().create_slot(int(dict_slot['iso_weekday']), dict_slot['time'], created_program)
            except Exception as e:
                created_program.delete()
                for created_slot in created_slots:
                    created_slot.delete()
                raise(e)

        return created_program
