from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Service
import json
from timer.models import Timer
from django.utils import timezone

def create_timer(service: Service, data: dict):
    if "time" in data:
        if not data["time"].isdigit():
            raise serializers.ValidationError("Timer must be a number")
        int_timer = int(data["time"])
        date_time = timezone.now() + timezone.timedelta(minutes=int_timer)
        timer = Timer.objects.filter(service=service).first()
        if timer:
            timer.date_time = date_time
        else:
            timer = Timer.objects.create(date_time=date_time, service=service)
        timer.save()
    else:
        raise serializers.ValidationError("timer not found in data")

def check_data_action(action_type: str, data: dict):
    try:
        file = open("about/about.json", "r")
        json_data = json.load(file)
        file.close()
    except:
        print("error while reading about.json")
        return None
    actions = Service.ACTIONS
    if not action_type in [action[0] for action in actions]:
        raise serializers.ValidationError("Action not valid")
    for service in json_data["server"]["services"]:
        for action in service["actions"]:
            if action["nickname"] == action_type and "action_data" in action:
                for action_data in action["action_data"]:
                    if not action_data["name"] in data:
                        raise serializers.ValidationError(f"{action_data['name']} not found in data")
                

def check_data_reaction(reaction_type: str, data: dict):
    try:
        file = open("about/about.json", "r")
        json_data = json.load(file)
        file.close()
    except:
        print("error while reading about.json")
        return None
    print("Working reaction")
    print(data)
    print(reaction_type)
    reactions = Service.REACTIONS
    if not reaction_type in [reaction[0] for reaction in reactions]:
        raise serializers.ValidationError("Reaction not valid")
    for service in json_data["server"]["services"]:
        for reaction in service["reactions"]:
            if reaction["nickname"] == reaction_type and "reaction_data" in reaction:
                for reaction_data in reaction["reaction_data"]:
                    if not reaction_data["name"] in data:
                        raise serializers.ValidationError(f"{reaction_data['name']} not found in data")

class AddServiceSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    action = serializers.CharField(max_length=4)
    reaction = serializers.CharField(max_length=4)
    action_data = serializers.JSONField()
    reaction_data = serializers.JSONField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data):
        user = validated_data.pop('user')
        for action_row in Service.ACTIONS:
            if action_row[0] == validated_data['action']:
                validated_data['name_action'] = action_row[1]
        for reaction_row in Service.REACTIONS:
            if reaction_row[0] == validated_data['reaction']:
                validated_data['name_reaction'] = reaction_row[1]
        check_data_action(validated_data['action'], validated_data['action_data'])
        check_data_reaction(validated_data['reaction'], validated_data['reaction_data'])
        service = Service.objects.create(owner=user, **validated_data)
        if validated_data['action'] == "ATI0":
            create_timer(service, validated_data['action_data'])
        return service

    def update(self, instance, validated_data):
        for action_row in Service.ACTIONS:
            if action_row[0] == validated_data['action']:
                instance.name_action = action_row[1]
        for reaction_row in Service.REACTIONS:
            if reaction_row[0] == validated_data['reaction']:
                instance.name_reaction = reaction_row[1]
        instance.name = validated_data.get('name', instance.name)
        instance.action = validated_data.get('action', instance.action)
        instance.reaction = validated_data.get('reaction', instance.reaction)
        instance.action_data = validated_data.get('action_data', instance.action_data)
        instance.reaction_data = validated_data.get('reaction_data', instance.reaction_data)
        check_data_action(instance.action, instance.action_data)
        check_data_reaction(instance.reaction, instance.reaction_data)
        instance.save()
        if validated_data['action'] == "ATI0":
            create_timer(instance, instance.action_data)
        else:
            timer = Timer.objects.filter(service=instance).first()
            if timer:
                timer.delete()
        return instance
    
class ServiceIdSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def validate(self, attrs):
        self.id = attrs.get('id')
        service = Service.objects.filter(id=self.id).first()
        if not service:
            raise serializers.ValidationError("Service not found")
        if service.owner != self.context['request'].user:
            raise serializers.ValidationError("You are not the owner of this service")
        return attrs

class ResponseServiceSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    action = serializers.CharField(max_length=4)
    reaction = serializers.CharField(max_length=4)
    name_action = serializers.CharField(max_length=100)
    name_reaction = serializers.CharField(max_length=100)
    action_data = serializers.JSONField()
    reaction_data = serializers.JSONField()

