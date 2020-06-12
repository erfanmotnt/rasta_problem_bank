from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from mhbank.models import Account
from mhbank.serializers import PrivateAccountSerializer, PublicAccountSerializer


class AccountView(APIView):
    def get(self, request):
        user_id = request.query_params.get('id')
        try:
            account = Account.objects.get(user_id=user_id)
        except Account.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PrivateAccountSerializer(account) if request.user == account.user \
            else PublicAccountSerializer(account)
        return Response(serializer.data)

    def post(self, request):
        serializer = PrivateAccountSerializer(data=request.data)
        serializer.initial_data['role'] = 'a'
        if not serializer.is_valid():
            print(serializer.errors)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        account = serializer.save()
        token = Token.objects.create(user=account.user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)

# @csrf_exempt
# def account_detail(request, pk):
#     try:
#         account = Account.objects.get(pk=pk)
#     except Account.DoesNotExist:
#         return HttpResponse(status=404)
#
#     if request.method == 'GET':
#         serializer = AccountSerializer(account)
#         return JsonResponse(serializer.data)
#
#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = AccountSerializer(account, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)
#
#     elif request.method == 'DELETE':
#         account.delete()
#         return HttpResponse(status=204)
#
#
# @csrf_exempt
# def account_list(request):
#     if request.method == 'GET':
#         account = Account.objects.all()
#         serializer = AccountSerializer(account, many=True)
#         return JsonResponse(serializer.data, safe=False)
#
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = AccountSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)
