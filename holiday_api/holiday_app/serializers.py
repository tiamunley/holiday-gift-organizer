from django.apps import apps
from rest_framework import serializers

from holiday_app.models import *


class GiftSerializer(serializers.HyperlinkedModelSerializer):
    """
    RW Gift Serializer
    """

    recipient = serializers.PrimaryKeyRelatedField(queryset=apps.get_model('holiday_app.Recipient').objects.all())

    class Meta:
        model = apps.get_model('holiday_app.Gift')
        fields = ('status', 'item', 'notes', 'cost',
                  'recipient', 'id')


class RecipientSerializer(serializers.HyperlinkedModelSerializer):
    """
    RW Recipient Serializer
    """

    # this field can be read or written, but the value must be in that queryset.
    giver = serializers.PrimaryKeyRelatedField(queryset=apps.get_model('holiday_app.HolidayUser').objects.all())

    # This will return the entire thing for each Gift (saves queries).
    gifts = GiftSerializer(many=True, read_only=True)

    class Meta:
        model = apps.get_model('holiday_app.Recipient')
        fields = ('name', 'giver', 'id', 'gifts',
                  'relation')


class HolidayUserSerializer(serializers.HyperlinkedModelSerializer):
    """
    RW HolidayUser serializer.
    """

    recipients = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    # input
    password = serializers.CharField(
        write_only=True,
        style={
            'input_type': 'password',
            'placeholder': 'Password'
        }
    )

    def create(self, validated_data):
        """
        Create the user.
        """

        user = HolidayUser.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = apps.get_model('holiday_app.HolidayUser')
        fields = ('added', 'email', 'username',
                  'password', 'first_name',
                  'last_name', 'recipients',
                  'id')
        write_only_fields = ('password',)


class LoginUserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Login output serializer.
    """

    class Meta:
        model = apps.get_model('holiday_app.HolidayUser')
        fields = ('email', 'username', 'first_name',
                  'last_name', 'id')




