from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import *
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from .authentication import JWTAuthentication


class CreateAccount(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        resp_dict = dict()
        resp_dict['status'] = False
        resp_dict['message'] = "Something went wrong. Please try again after sometime"
        try:
            create_user_manager = UserAccountManager(request)
            save_user_resp = create_user_manager.start_on_boarding()
            resp_dict['status'] = save_user_resp['status']
            resp_dict['message'] = save_user_resp['message']
        except Exception as e:
            logging.error('Error in creating account', repr(e))
        return JsonResponse(resp_dict, status=200)


class Login(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is None:
            raise AuthenticationFailed('Invalid credentials')

        payload = {
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(days=1)
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return Response({'token': token}, status=status.HTTP_200_OK)


class Deposit(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        resp_dict = dict()
        resp_dict['status'] = False
        resp_dict['message'] = "Something went wrong. Please try again after sometime"
        try:
            deposit_manager = UserAccountManager(request)
            save_user_resp = deposit_manager.deposit()
            resp_dict['status'] = save_user_resp['status']
            resp_dict['message'] = save_user_resp['message']
            resp_dict['data'] = save_user_resp['data']
        except Exception as e:
            logging.error('Error in depositing', repr(e))
        return JsonResponse(resp_dict, status=200)


class Withdrawal(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        resp_dict = dict()
        resp_dict['status'] = False
        resp_dict['message'] = "Something went wrong. Please try again after sometime"
        try:
            deposit_manager = UserAccountManager(request)
            save_user_resp = deposit_manager.withdrawal()
            resp_dict['status'] = save_user_resp['status']
            resp_dict['message'] = save_user_resp['message']
            resp_dict['data'] = save_user_resp['data']
        except Exception as e:
            logging.error('Error in withdrawing', repr(e))
        return JsonResponse(resp_dict, status=200)


class TransactionHistory(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        resp_dict = dict()
        resp_dict['status'] = False
        resp_dict['message'] = "Something went wrong. Please try again after sometime"
        try:
            transaction_history_manager = UserAccountManager(request)
            save_user_resp = transaction_history_manager.transaction_history()
            resp_dict['status'] = save_user_resp['status']
            resp_dict['message'] = save_user_resp['message']
            resp_dict['data'] = save_user_resp['data']
        except Exception as e:
            logging.error('Error in Transaction History', repr(e))
        return JsonResponse(resp_dict, status=200)


class GetWalletBalance(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        resp_dict = dict()
        resp_dict['status'] = False
        resp_dict['message'] = "Something went wrong. Please try again after sometime"
        try:
            wallet_balance_manager = UserAccountManager(request)
            save_user_resp = wallet_balance_manager.wallet_balance_details()
            resp_dict['status'] = save_user_resp['status']
            resp_dict['message'] = save_user_resp['message']
            resp_dict['data'] = save_user_resp['data']
        except Exception as e:
            logging.error('Error in getting wallet balance', repr(e))
        return JsonResponse(resp_dict, status=200)