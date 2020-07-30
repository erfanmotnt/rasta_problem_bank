from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User

from mhbank.models import Account
from mhbank.serializers import PrivateAccountSerializer, PublicAccountSerializer
from mhbank.views import permissions


class AccountView(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin):
    permission_classes = [permissions.AccountPermission]
    queryset = Account.objects.all()

    def get_serializer_class(self):
        return PrivateAccountSerializer \
            if self.request.user.account.id == int(self.request.parser_context['kwargs'].get('pk', -1)) \
            else PublicAccountSerializer

@api_view()
def account_by_username(request):
    try:
        account = request.user.account
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    a_serializer = PrivateAccountSerializer(account)
    return Response(a_serializer.data, status=status.HTTP_200_OK)
