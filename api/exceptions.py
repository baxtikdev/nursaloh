from rest_framework.exceptions import APIException


class ProductNotFoundException(APIException):
    status_code = 400
    default_detail = 'Product does not exist'
