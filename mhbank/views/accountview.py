from rest_framework import viewsets
from rest_framework import mixins

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
