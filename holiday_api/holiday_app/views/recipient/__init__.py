from rest_framework import viewsets

from holiday_app.serializers import RecipientSerializer
from holiday_app.models import Recipient


class RecipientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows recipients to be viewed or edited.
    """

    queryset = Recipient.objects.all()
    serializer_class = RecipientSerializer


