"""
Custom defined exceptions
"""
from rest_framework import status
from rest_framework.exceptions import APIException


class NotEnoughCashError(APIException):
    default_code = 'invalid'
    default_detail = {'message': 'Not enough cash to purchase stock', 'status': status.HTTP_400_BAD_REQUEST}
    status_code = status.HTTP_400_BAD_REQUEST


class StockNotPresentError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'invalid'
    default_detail = {'message': 'You have not purchased stock of this company', 'status': status.HTTP_400_BAD_REQUEST}

    def __init__(self, company: str):
        super()
        self.detail = {'status': status.HTTP_400_BAD_REQUEST,
                       'detail': f'You have not purchased any shares of {company}'}


class NotEnoughStockError(APIException):
    code = status.HTTP_400_BAD_REQUEST
    default_code = 'invalid'

    def __init__(self, company: str, quantity: int):
        super()
        self.detail = {'status': status.HTTP_400_BAD_REQUEST,
                       'detail': f'You have purchased only {quantity} shares of company {company}'}
