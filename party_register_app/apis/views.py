# registration/apis/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from party_register_app.models import Guest
from .serializers import GuestSerializer


class GuestViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows guests to be viewed or created.
    Also provides a custom action to check-in a guest.
    """
    queryset = Guest.objects.all().order_by('-created_at')
    serializer_class = GuestSerializer
    lookup_field = 'unique_id'

    @action(detail=True, methods=['post'], url_path='check-in')
    def check_in(self, request, unique_id=None):
        guest = self.get_object()
        if guest.status == Guest.Status.ENTERED:
            return Response(
                {'status': 'error', 'message': 'Guest has already been checked in.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        guest.status = Guest.Status.ENTERED
        guest.save()

        serializer = self.get_serializer(guest)
        return Response(serializer.data)
