from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import logout
from mhbank.serializers import PrivateAccountSerializer


@api_view(['POST'])
def register(request):
    serializer = PrivateAccountSerializer(data=request.data)
    serializer.initial_data['role'] = 'a'
    if not serializer.is_valid():
        print(serializer.errors)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    account = serializer.save()
    token = Token.objects.create(user=account.user)
    return Response({'token': token.key}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@action(detail=False, methods=['post'])
def signout(request):
    try:
        request.user.auth_token.delete()
    except (AttributeError, ObjectDoesNotExist):
        pass
    logout(request)
    return Response(status=status.HTTP_200_OK)