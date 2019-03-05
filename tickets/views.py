from django.contrib.auth.models import User
from .models import Ticket
from .serializers import TicketSerializer, UserSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


class TicketViewSet(viewsets.ModelViewSet):
    """
    Этот вьюсет автоматически настраивает `list`, `create`, `retrieve`,
    `update` и `destroy` действия.

    """
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Этот вьюсет автоматически настраивает `list` and `detail` действия.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TicketAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
