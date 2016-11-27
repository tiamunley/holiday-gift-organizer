from rest_framework import viewsets

from holiday_app.serializers import HolidayUserSerializer
from holiday_app.models import HolidayUser


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows recipients to be viewed or edited.
    """

    queryset = HolidayUser.objects.all()
    serializer_class = HolidayUserSerializer


