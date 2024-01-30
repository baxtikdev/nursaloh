import hashlib

from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsClient
from common.order.models import Order, OrderStatus
from common.payment.models import Payment, PaymentType, PaymentStatus
from config.settings.base import env


def isset(data, columns):
    for column in columns:
        if data.get(column, None):
            return False
    return True


def orderLoad(id):
    try:
        return Order.objects.get(id=id)
    except:
        return None


def click_secret_key():
    PAYMENT_VARIANTS = settings.PAYMENT_VARIANTS
    _click = PAYMENT_VARIANTS['click']
    secret_key = _click[1]['secret_key']
    return secret_key


@extend_schema(tags=["Click"])
class PaymentClick(APIView):
    permission_classes = [IsClient]

    def get(self, request):
        id = request.query_params.get('id')
        if id is None:
            return Response({"error": "Order id does not found"}, status=status.HTTP_400_BAD_REQUEST)
        order = Order.objects.filter(id=id, user=request.user).first()
        if order is None:
            return Response({"error": "Order does not found"}, status=status.HTTP_400_BAD_REQUEST)
        context = {
            'merchant_id': env('CLICK_MERCHANT_ID'),
            'service_id': env('CLICK_SERVICE_ID'),
            'amount': order.totalAmount,
            'transaction_param': order.id
        }
        return Response(context, status=status.HTTP_200_OK)


@extend_schema(tags=["Click"])
class PaymentPrepareAPIView(APIView):

    def post(self, request, *args, **kwargs):
        orderID = request.data.get('merchant_trans_id', None)
        result = self.click_webhook_errors(request)
        order = orderLoad(orderID)
        if result['error'] == '0' and order:
            order.status = OrderStatus.PAYMENT
            order.save()
        result['click_trans_id'] = request.data.get('click_trans_id', None)
        result['merchant_trans_id'] = request.data.get('merchant_trans_id', None)
        result['merchant_prepare_id'] = request.data.get('merchant_trans_id', None)
        result['merchant_confirm_id'] = request.data.get('merchant_trans_id', None)
        return Response(result, status=status.HTTP_200_OK)

    def click_webhook_errors(self, request):
        click_trans_id = request.data.get('click_trans_id', None)
        service_id = request.data.get('service_id', None)
        orderID = request.data.get('merchant_trans_id', None)
        amount = request.data.get('amount', None)
        action = request.data.get('action', None)
        error = request.data.get('error', None)
        sign_time = request.data.get('sign_time', None)
        sign_string = request.data.get('sign_string', None)
        merchant_prepare_id = request.data.get('merchant_prepare_id', None) if action != None and action == '1' else ''
        if isset(request.data,
                 ['click_trans_id', 'service_id', 'click_paydoc_id', 'amount', 'action', 'error', 'error_note',
                  'sign_time',
                  'sign_string']) or (
            action == '1' and isset(request.data, ['merchant_prepare_id'])):
            return {
                'error': '-8',
                'error_note': 'Error in request from click'
            }

        signString = '{}{}{}{}{}{}{}{}'.format(
            click_trans_id, service_id, click_secret_key(), orderID, merchant_prepare_id, amount, action, sign_time
        )
        encoder = hashlib.md5(signString.encode('utf-8'))
        signString = encoder.hexdigest()

        if signString != sign_string:
            return {
                'error': '-1',
                'error_note': 'SIGN CHECK FAILED!'
            }

        if action not in ['0', '1']:
            return {
                'error': '-3',
                'error_note': 'Action not found'
            }

        order = orderLoad(orderID)
        if order is None:
            return {
                'error': '-5',
                'error_note': 'User does not exist'
            }
        if abs(float(order.totalAmount) - float(amount) > 0.01) or float(order.totalAmount) > float(amount) or float(
            order.totalAmount) <= 0:
            return {
                'error': '-2',
                'error_note': 'Incorrect parameter amount'
            }

        if order.paymentStatus == PaymentStatus.CONFIRMED:
            return {
                'error': '-4',
                'error_note': 'Already paid'
            }

        if action == '1':
            if orderID != merchant_prepare_id:
                return {
                    'error': '-6',
                    'error_note': 'Transaction not found'
                }

        if order.paymentStatus == PaymentStatus.REJECTED or int(error) < 0:
            return {
                'error': '-9',
                'error_note': 'Transaction cancelled'
            }
        return {
            'error': '0',
            'error_note': 'Success'
        }


@extend_schema(tags=["Click"])
class PaymentCompleteAPIView(APIView):

    def post(self, request, *args, **kwargs):
        orderID = request.data.get('merchant_trans_id', None)
        order = orderLoad(orderID)
        result = self.click_webhook_errors(request)
        if request.data.get('error', None) != None and int(request.data.get('error', None)) < 0 and order:
            order.paymentStatus = PaymentStatus.ERROR
            order.save()
        if result['error'] == '0' and order:
            order.status = OrderStatus.PENDING
            order.paymentStatus = PaymentStatus.CONFIRMED
            order.paymentType = PaymentType.CLICK
            order.save()

            Payment.objects.create(
                user=order.user,
                order=order,
                amount=order.totalAmount,
                paymentType=PaymentType.CLICK,
                status=PaymentStatus.CONFIRMED
            )

        result['click_trans_id'] = request.data.get('click_trans_id', None)
        result['merchant_trans_id'] = request.data.get('merchant_trans_id', None)
        result['merchant_prepare_id'] = request.data.get('merchant_prepare_id', None)
        result['merchant_confirm_id'] = request.data.get('merchant_prepare_id', None)
        return Response(result)

    def click_webhook_errors(self, request):
        click_trans_id = request.data.get('click_trans_id', None)
        service_id = request.data.get('service_id', None)
        click_paydoc_id = request.data.get('click_paydoc_id', None)
        orderID = request.data.get('merchant_trans_id', None)
        amount = request.data.get('amount', None)
        action = request.data.get('action', None)
        error = request.data.get('error', None)
        error_note = request.data.get('error_note', None)
        sign_time = request.data.get('sign_time', None)
        sign_string = request.data.get('sign_string', None)
        merchant_prepare_id = request.data.get('merchant_prepare_id', None) if action != None and action == '1' else ''
        if isset(request.data,
                 ['click_trans_id', 'service_id', 'click_paydoc_id', 'amount', 'action', 'error', 'error_note',
                  'sign_time',
                  'sign_string']) or (
            action == '1' and isset(request.data, ['merchant_prepare_id'])):
            return {
                'error': '-8',
                'error_note': 'Error in request from click'
            }

        signString = '{}{}{}{}{}{}{}{}'.format(
            click_trans_id, service_id, click_secret_key(), orderID, merchant_prepare_id, amount, action, sign_time
        )
        encoder = hashlib.md5(signString.encode('utf-8'))
        signString = encoder.hexdigest()

        if signString != sign_string:
            return {
                'error': '-1',
                'error_note': 'SIGN CHECK FAILED!'
            }

        if action not in ['0', '1']:
            return {
                'error': '-3',
                'error_note': 'Action not found'
            }

        order = orderLoad(orderID)
        if order is None:
            return {
                'error': '-5',
                'error_note': 'User does not exist'
            }
        if abs(float(order.totalAmount) - float(amount) > 0.01) or float(order.totalAmount) > float(amount) or float(
            order.totalAmount) <= 0:
            return {
                'error': '-2',
                'error_note': 'Incorrect parameter amount'
            }

        if order.paymentStatus == PaymentStatus.CONFIRMED:
            return {
                'error': '-4',
                'error_note': 'Already paid'
            }

        if action == '1':
            if orderID != merchant_prepare_id:
                return {
                    'error': '-6',
                    'error_note': 'Transaction not found'
                }

        if order.paymentStatus == PaymentStatus.REJECTED or int(error) < 0:
            return {
                'error': '-9',
                'error_note': 'Transaction cancelled'
            }
        return {
            'error': '0',
            'error_note': 'Success'
        }
