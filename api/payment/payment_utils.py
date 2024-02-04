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

def create_initialization_click(amount: Decimal, order_id: str):
    return f"https://my.click.uz/services/pay?service_id=28420&merchant_id=11369&return_url=https://kale.uz/profile/purchases-history&amount={amount}&transaction_param={order_id}"
