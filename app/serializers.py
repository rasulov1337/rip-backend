from django.contrib.auth.models import User

from app.models import Recipient, FileTransfer, FileTransferRecipient
from rest_framework import serializers


class RecipientSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Recipient
        # Поля, которые мы сериализуем
        fields = ["id", "name", "desc", "phone", "city", "birthdate", "status", "avatar", "uni"]


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

    class Meta:
        model = User
        fields = '__all__'


class FileTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileTransfer
        fields = '__all__'

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['sender'] = User.objects.get(id=repr['sender']).username
        if repr['moderator']:
            repr['moderator'] = User.objects.get(id=repr['moderator']).username

        res = []
        for recipient in instance.recipients.all():
            res.append({'id': recipient.id,
                        'name': recipient.name,
                        'phone': recipient.phone,
                        'avatar': recipient.avatar})
        repr['recipients'] = res
        return repr

    def update(self, instance, validated_data):
        instance.file = validated_data.get('file', instance.file)
        instance.save()
        return instance


class FileTransferRecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileTransferRecipient
        read_only_fields = ['file_transfer', 'recipient', 'sent_at']
        fields = '__all__'