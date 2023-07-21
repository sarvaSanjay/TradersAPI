"""
Useful functions
"""
import requests
from rest_framework import status
from rest_framework.exceptions import APIException


def get_stock_price(name: str):

    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-summary"

    querystring = {"symbol": f'{name}', "region": "US"}

    headers = {
        "X-RapidAPI-Key": "b2ec853cbbmshf8a3288593c53c7p1c695bjsn08a2c975a1e3",
        "X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    try:
        current_price = data['financialData']['currentPrice']['raw']
    except KeyError:
        raise InvalidStockException
    else:
        return current_price


class InvalidStockException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid company name"
    default_code = "invalid"
