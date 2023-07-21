from django.db.models import QuerySet
from django.http import JsonResponse
from rest_framework import views, status
from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import yfinance as yf

from Traders.exceptions import NotEnoughCashError, NotEnoughStockError, StockNotPresentError
from Traders.models import History, Stock
from Traders.response_model import response_model
from Traders.serializers import HistorySerializer, StockSerializer
from Traders.utils import get_stock_price


# Create your views here.
class CashView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = self.request.user
        response = response_model(status=status.HTTP_200_OK,
                                  message="cash and username details listed",
                                  details={'cash': user.cash, 'username': user.username})
        return Response(status=status.HTTP_200_OK, data=response)


class StocksView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            user = self.request.user
            stocks = Stock.objects.filter(user=user)
            deserialized_data = StockSerializer(stocks, many=True)
            response = response_model(status=status.HTTP_200_OK, message='all share details listed', details=deserialized_data.data)
            return Response(data=response, status=status.HTTP_200_OK)
        except:
            response = response_model(status=status.HTTP_400_BAD_REQUEST, message='unable to fetch share details')
            return Response(status=status.HTTP_400_BAD_REQUEST, data=response)

class BuyView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = self.request.user
        data = JSONParser().parse(request)
        serialized_data = StockSerializer(data=data)
        if not serialized_data.is_valid(raise_exception=True):
            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
        price = get_stock_price(data["company"])
        total_cost = round(price * data["quantity"], 2)
        if total_cost > user.cash:
            raise NotEnoughCashError(code=status.HTTP_400_BAD_REQUEST)
        user.cash -= total_cost
        stocks = Stock.objects.filter(user=user).filter(company=data["company"])
        if stocks:
            stock = stocks[0]
            stock.quantity += data["quantity"]
        else:
            stock = Stock(company=data["company"], quantity=data["quantity"], user=user)
            user.save()
        stock.save()
        history = History(company=data["company"], quantity=data["quantity"], user=user, price=price, type="B")
        history.save()
        response = response_model(status=status.HTTP_201_CREATED,
                                  message=f'{stock.quantity} shares of {stock.company} bought for user {user.username}',
                                  details={'totalCost': total_cost,
                                           'balanceCash': user.cash})
        return Response(status=status.HTTP_201_CREATED, data=response)


class SellView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = self.request.user
        data = JSONParser().parse(request)
        stock_serialiser = StockSerializer(data=data)
        if not stock_serialiser.is_valid(raise_exception=True):
            return Response(stock_serialiser.errors, status=status.HTTP_400_BAD_REQUEST)
        stocks: QuerySet[Stock] = user.stock_set.filter(company=data["company"])
        if not stocks:
            raise StockNotPresentError(company=data['company'])
        stock: Stock = stocks[0]
        if stock.quantity < data['quantity']:
            raise NotEnoughStockError(company=data['company'], quantity=data['quantity'])
        elif stock.quantity == data['quantity']:
            stock.delete()
        else:
            stock.quantity -= data['quantity']
            stock.save()
        price = get_stock_price(stock.company)
        total_cost = round(data['quantity'] * price, 2)
        user.cash += total_cost
        user.save()
        history = History(company=data["company"], quantity=data["quantity"], user=user, price=price, type="S")
        history.save()
        response = response_model(status=status.HTTP_201_CREATED,
                                  message=f'{stock.quantity} shares of {stock.company} sold for user {user.username}',
                                  details={'totalCost': total_cost,
                                           'balanceCash': user.cash})
        return Response(status=status.HTTP_201_CREATED)


class HistoryView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = self.request.user
        history = History.objects.filter(user=user)
        data = HistorySerializer(history, many=True).data
        response = response_model(status=status.HTTP_200_OK,
                                  message=f'Transaction history for {user.username} listed',
                                  details=data)
        return Response(status=status.HTTP_200_OK, data=response)
