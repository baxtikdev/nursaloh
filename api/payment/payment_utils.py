from decimal import Decimal


# PAYME_ID = settings.PAYME_SETTINGS['ID']
# KEY = "order_id"

# LINK = 'https://checkout.paycom.uz'


# def create_initialization_payme(amount: Decimal, order_id: str) -> str:
#     amount = amount * 100
#     params = f"m={PAYME_ID};ac.{KEY}={order_id};a={amount};c=https://kale.uz/profile/purchases-history"
#     encode_params = base64.b64encode(params.encode("utf-8"))
#     encode_params = str(encode_params, 'utf-8')
#     url = f"{LINK}/{encode_params}"
#     return url


# CLICK_PAYMENT_HOST=nursaloh.doppidev.uz
# CLICK_MERCHANT_ID=21049
# CLICK_SERVICE_ID=32155
# CLICK_MERCHANT_USER_ID=39083
# CLICK_SECRET_KEY=WCnIUlI3Ihdj


def create_initialization_click(amount: Decimal, order_id: str):
    return f"https://my.click.uz/services/pay?service_id=32155&merchant_id=21049&return_url=https://nursaloh.doppidev.uz/profile/history&amount={amount}&transaction_param={order_id}"
