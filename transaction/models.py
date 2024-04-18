from django.db import models
from django.conf import settings
from accounts.models import CustomUser
import logging
import re

class BankAccount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='bankaccount', on_delete=models.CASCADE, )
    account_balance = models.FloatField(default=0)
    date = models.DateTimeField(auto_now=True, verbose_name='Transaction Date')

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.user


class Transactions(models.Model):
    transaction_type = (
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, )
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, )
    transaction_type = models.CharField(max_length=20, choices=transaction_type)
    transaction_amount = models.FloatField()
    transaction_date = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        ordering = ['-transaction_date']

    def __str__(self):
        return self.transaction_type


class UserSignupValidation:

    def validate_signup_data(self, username, email):
        errors = {}
        if not username or email.strip() == "":
            errors = 'Username is required'
        elif not email or email.strip() == "":
            errors = 'Email address is required'
        elif CustomUser.objects.filter(username=username).exists():
            errors = 'Username is already in use'
        elif CustomUser.objects.filter(email=email).exists():
            errors = 'Email address is already in use'

        email_regex = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

        if not email_regex.match(email):
            errors = 'Please provide a valid email address (e.g., username@gmail.com)'

        if errors:
            return {'resp_dict': {'status': False, 'message': errors}}
        return {'resp_dict': {'status': True, 'message': 'Validation successful'}}


class UserAccountManager:
    def __init__(self, request):
        self.request = request

    def start_on_boarding(self):
        username = self.request.data.get('username')
        email = self.request.data.get('email')
        password = self.request.data.get('password')
        phone_number = self.request.data.get('phone_number', None)
        account_balance = self.request.data.get('account_balance', 0)
        validator = UserSignupValidation()
        validation_result = validator.validate_signup_data(username, email)
        resp_dict = validation_result['resp_dict']
        if not resp_dict['status']:
            return resp_dict

        try:

            user = CustomUser.objects.create_user(username=username, email=email, password=password, phone_number=phone_number)
            BankAccount.objects.create(user=user, account_balance=account_balance)
            resp_dict.update({
                'status': True,
                'message': 'User account created successfully'
            })
        except Exception as e:
            logging('getting exception on start_on_boarding', repr(e))
        return resp_dict

    def deposit(self):
        resp_dict = {'status': False, 'message': 'Something went wrong. Please try again later.', 'data':{}}
        amount = self.request.data.get('amount')
        try:
            if amount > 0:

                bank_account = BankAccount.objects.get(user=self.request.user)

                new_balance = bank_account.account_balance + amount
                bank_account.account_balance = new_balance
                bank_account.save()
                Transactions.objects.create(
                    user=self.request.user,
                    bank_account=bank_account,
                    transaction_type='deposit',
                    transaction_amount=amount
                )

                resp_dict.update({
                    'status': True,
                    'message': 'Deposit successful',
                    'data': {'new_balance': new_balance}
                })

        except Exception as e:
            logging('getting exception on deposit', repr(e))
        return resp_dict

    def withdrawal(self):
        resp_dict = {'status': False, 'message': 'Something went wrong. Please try again later.', 'data': {}}
        amount = self.request.data.get('amount')

        if amount <= 0:
            resp_dict['message'] = 'Invalid withdrawal amount'
            resp_dict['status'] = 'False'

        try:
            bank_account = BankAccount.objects.get(user=self.request.user)

            if bank_account.account_balance < amount:
                resp_dict['message'] = 'Insufficient balance'
                resp_dict['status'] = 'False'
            else:
                new_balance = bank_account.account_balance - amount
                bank_account.account_balance = new_balance
                bank_account.save()
                Transactions.objects.create(
                    user=self.request.user,
                    bank_account=bank_account,
                    transaction_type='withdrawal',
                    transaction_amount=amount
                )

                resp_dict.update({
                    'status': True,
                    'message': 'Withdrawal successful',
                    'data': {'new_balance': new_balance}
                })
        except Exception as e:
            logging('getting exception on withdrawal', repr(e))

        return resp_dict

    def transaction_history(self):
        resp_dict = {'status': False, 'message': 'Something went wrong. Please try again later.', 'data': {}}
        try:
            transactions = Transactions.objects.filter(user=self.request.user).order_by('-transaction_date')
            transaction_data = []
            for transaction in transactions:
                transaction_data.append({
                    'transaction_type': transaction.transaction_type,
                    'transaction_amount': transaction.transaction_amount,
                    'transaction_date': transaction.transaction_date
                })
            resp_dict['status'] = True
            resp_dict['message'] = "Got data successfully"
            resp_dict['data'] = transaction_data
        except Exception as e:
            logging('getting exception on transaction_history', repr(e))

        return resp_dict

    def wallet_balance_details(self):
        resp_dict = {'status': False, 'message': 'Something went wrong. Please try again later.', 'data': {}}
        try:
            bank_account = BankAccount.objects.get(user=self.request.user)
            resp_dict['status'] = True
            resp_dict['message'] = "Got data successfully"
            resp_dict['data']['total_balance'] = bank_account.account_balance
        except Exception as e:
            logging('getting exception on wallet_balance_details', repr(e))

        return resp_dict