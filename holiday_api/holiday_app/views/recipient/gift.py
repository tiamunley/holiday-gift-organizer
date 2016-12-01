from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from holiday_app.serializers import GiftSerializer
from holiday_app.models import Gift


class GiftViewSet(viewsets.ModelViewSet):
    """
    API endpoint which deals with recipient/{pk}/gift/{pk}
    """

    queryset = Gift.objects.all()
    serializer_class = GiftSerializer

    def list(self, request, recipient_pk=None, **kwargs):
        """
        List all the Gifts for a specific recipient.  Technically just retrieving the Recipient will provide this.
        """

        queryset = Gift.objects.all()
        serializer = GiftSerializer(queryset.filter(recipient=recipient_pk), many=True, context={'request': request})

        return Response(serializer.data)

    def create(self, request, recipient_pk=None, **kwargs):
        """
        Create a gift for a recipient.
        """

        new_data = request.data.copy()
        new_data['recipient'] = recipient_pk

        serializer = GiftSerializer(data=new_data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, recipient_pk=None, **kwargs):
        """
        Retrieve a specific gift for a recipient.
        """

        gift = get_object_or_404(Gift.objects.all(), pk=pk)
        serializer = GiftSerializer(gift)

        return Response(serializer.data)

    def update(self, request, pk=None, recipient_pk=None, **kwargs):
        """
        Update a specific gift for a recipient.
        """

        obj = Gift.objects.get(pk=pk)

        new_data = request.data.copy()
        # XXX: This prevents you from changing the parent recipient.
        new_data['recipient'] = obj.recipient.id

        serializer = GiftSerializer(obj, data=new_data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None, **kwargs):
        """
        Let's not bother supporting PATCH.
        """

        return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None, recipient_pk=None, **kwargs):
        """
        Delete the Gift.
        """

        Gift.objects.get(pk=pk).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
