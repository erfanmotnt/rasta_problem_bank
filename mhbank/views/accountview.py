from rest_framework import viewsets

from mhbank.models import Account
from mhbank.serializers import PrivateAccountSerializer, PublicAccountSerializer


class AccountView(viewsets.ModelViewSet):
    queryset = Account.objects.all()

    def get_serializer_class(self):
        return PrivateAccountSerializer \
            if self.request.user.account.id == int(self.request.parser_context['kwargs'].get('pk', -1)) \
            else PublicAccountSerializer

    # def retrieve(self, request, *args, **kwargs):
    #     account_id = kwargs['pk']
    #     try:
    #         account = Account.objects.get(id=account_id)
    #     except Account.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #     serializer = self.get_serializer(account)
    #     return Response(serializer.data)

