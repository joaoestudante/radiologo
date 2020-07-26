from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from .SlotSerializer import SlotSerializer
from ..models import Program
from ..services.ProgramService import ProgramService
from ..services.SlotService import SlotService


class AuthorsField(serializers.RelatedField):
    def to_representation(self, value):
        return {"id": value.pk, "author_name": value.author_name}

    def to_internal_value(self, data):
        return data["id"]


class ProgramSerializer(serializers.ModelSerializer):
    slot_set = SlotSerializer(many=True)
    authors = AuthorsField(many=True, queryset=get_user_model().objects.all())

    class Meta:
        model = Program
        fields = ['id', 'name', 'normalized_name', 'description', 'max_duration', 'first_emission_date', 'comes_normalized',
                  'ignore_duration_adjustment', 'is_external', 'state', 'slot_set', 'enabled_days', 'next_upload_date',
                  'authors']

    @transaction.atomic
    def create(self, validated_data):
        slots_data = validated_data.pop('slot_set')
        authors_data = validated_data.pop('authors')
        created_program = ProgramService().create_program(authors_data, **validated_data)
        self.create_slots_from_data(slots_data, created_program)
        return created_program

    @transaction.atomic
    def update(self, instance, validated_data):
        if "slot_set" in validated_data:
            slots_data = validated_data.pop('slot_set')
            previous_slots = instance.slot_set.all()
            previous_slots.delete()
            self.create_slots_from_data(slots_data, instance)

        if "authors" in validated_data:
            authors = validated_data.pop('authors')
            instance.authors.set(authors)

        self.update_other_instance_fields(instance, validated_data)
        instance.save()

        return instance

    @staticmethod
    def update_other_instance_fields(instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.max_duration = validated_data.get('max_duration', instance.max_duration)
        instance.first_emission_date = validated_data.get('first_emission_date', instance.first_emission_date)
        instance.comes_normalized = validated_data.get('comes_normalized', instance.comes_normalized)
        instance.ignore_duration_adjustment = validated_data.get('ignore_duration_adjustment',
                                                                 instance.ignore_duration_adjustment)
        instance.is_external = validated_data.get('is_external', instance.is_external)
        instance.state = validated_data.get('state', instance.state)

    @staticmethod
    def create_slots_from_data(slots_data, created_program):
        for slot in slots_data:
            dict_slot = dict(slot)
            SlotService().create_slot(iso_weekday=int(dict_slot['iso_weekday']), time=dict_slot['time'],
                                      is_rerun=dict_slot.get("is_rerun", False), program_object=created_program)
