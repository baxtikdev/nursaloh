from celery import shared_task
from django.contrib.auth import get_user_model

from api.auth.send_sms_func import sent_sms_base
from common.product.models import Product, Category, SubCategory
from common.users.models import Code

User = get_user_model()


@shared_task(name='send_sms')
def send_sms(id, phone):
    user = User.objects.get(id=id)
    code, created = Code.objects.get_or_create(user=user)
    number = code.generate_code()
    sent_sms_base(code.user.id, number, phone)


@shared_task(name='verified_user')
def verified_user(guid):
    user = User.objects.get(guid=guid)
    user.is_verified = True
    user.save()


@shared_task(name='deleteProducts')
def deleteProducts():
    for i in Product.objects.all():
        i.delete()


# @shared_task(name='updateProducts')
# def updateProducts():
#     products = get_products()
#     newProducts = []
#     updateProducts = []
#     for product in products.get("Товары"):
#         category_name = product.get("Категория")
#         quantity = product.get("Остаток")
#         code = product.get("Код")
#         price = product.get("Цена")
#         title = product.get("Наименование")
#         unit = product.get("ЕдиницаИзмерения")
#         brand = product.get("ТорговаяМарка")
#         size = product.get("Размеры")
#         description = product.get("Описание")
#         manufacturer = product.get("Производитель")
#         if category_name and code and price > 0 and quantity > 0 and title:
#             category = SubCategory.objects.filter(title_ru=category_name).first()
#             if category is None:
#                 continue
#
#             pr = Product.objects.filter(code=code).first()
#             if pr and pr.code == code and pr.quantity < quantity:
#                 updateProducts.append(Product(
#                     id=pr.id,
#                     subcategory=category,
#                     # title=title,
#                     title_ru=title,
#                     description_ru=description,
#                     price=price,
#                     # material_ru=material,
#                     unit=unit,
#                     brand=brand,
#                     size=size,
#                     manufacturer_ru=manufacturer,
#                     quantity=quantity
#                 ))
#             elif pr is None:
#                 newProducts.append(Product(
#                     subcategory=category,
#                     code=code,
#                     # title=title,
#                     title_ru=title,
#                     description_ru=description,
#                     price=price,
#                     # material_ru=material,
#                     unit=unit,
#                     brand=brand,
#                     size=size,
#                     manufacturer_ru=manufacturer,
#                     quantity=quantity
#                 ))
#     if newProducts:
#         Product.objects.bulk_create(newProducts)
#     if updateProducts:
#         Product.objects.bulk_update(updateProducts,
#                                     fields=['subcategory', 'title_ru', 'description_ru', 'price', 'unit', 'brand',
#                                             'size',
#                                             'manufacturer_ru', 'quantity'])
#     return


categories = [
    {
        "title": "Унитаз",
        "subcategories": ["Унитаз подвесной", "Унитаз смарт", "Унитаз стоячий", "Биде подвесной", "Биде стоячий"]
    },
    {
        "title": "Смеситель",
        "subcategories": ['Смеситель встроенный', 'Смеситель для биде', 'Смеситель для ванны', 'Смеситель для раковины',
                          'Смеситель кухонный', 'Смеситель для душа', 'Смеситель от пола']
    },
    {
        "title": "Раковина",
        "subcategories": ["Раковина"]
    },
    {
        "title": "Мебель для ванной комнаты",
        "subcategories": ["Пенал", "Шкаф"]
    },
    {
        "title": "Кафель",
        "subcategories": ["Декор", "Кафель половой", "Кафель стеновой"]
    },
    {
        "title": "Калесинтерфлекс",
        "subcategories": ["Калесинтерфлекс"]
    },
    {
        "title": "Инсталляции",
        "subcategories": ["Инсталляции", "Кнопка"]
    },
    {
        "title": "Душевая система",
        "subcategories": ["Душ система", "Лейка со стойкойй", "Лейка", "Шланг"]
    },
    {
        "title": "Ванна",
        "subcategories": ["Ванна", "Ванна отдельностоящая", "Джакузи", "Душевая кабина" "Поддоны и перегородки"]
    },
    {
        "title": "Аксессуары и прочие",
        "subcategories": ["Аксессуары", "Гофра", "Сифон"]
    },
    {
        "title": "Полотенцесущитель",
        "subcategories": ["Полотенцесущитель"]
    },
    {
        "title": "Трапы",
        "subcategories": ["Трапы"]
    }
]


@shared_task(name='createCategories')
def createCategories():
    subcategories = []
    for i in categories:
        category, created = Category.objects.get_or_create(title_ru=i.get('title'))
        if created:
            for j in i.get('subcategories'):
                subcategories.append(SubCategory(category=category, title_ru=j))
    if subcategories:
        SubCategory.objects.bulk_create(subcategories)
