Api Documention of Wallet App:
creating account:
url:http://localhost:8000/transaction/create-account/
body:
{
    "username":"tarun",   
    "password":"tarun",
    "email":"t@gmail.com",
    "account_balance":200

}
Login:
url:http://localhost:8000/transaction/login/
{
   "username":"tarun",   
    "password":"tarun"
}
Deposit:
url:http://localhost:8000/transaction/deposit/
body:
{
    "amount":10
}
Withdrawal:
url:http://localhost:8000/transaction/withdrawal/
body:
{
    "amount":100
}
Get Transaction History:
url:http://localhost:8000/transaction/get-transaction-history/
reponse:
{
    "status": true,
    "message": "Got data successfully",
    "data": [
        {
            "transaction_type": "deposit",
            "transaction_amount": 10.0,
            "transaction_date": "2024-04-18T08:01:13.765Z"
        },
        {
            "transaction_type": "deposit",
            "transaction_amount": 10.0,
            "transaction_date": "2024-04-18T07:12:30.968Z"
        },
   
    ]
}
Get Wallet Balance:
url: http://localhost:8000/transaction/get-wallet-balance/
body:
{
    "status": true,
    "message": "Got data successfully",
    "data": {
        "total_balance": 200.0
    }
}
