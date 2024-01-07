import re

from celery import shared_task
from django.contrib.auth import get_user_model
from tablib import Dataset

from api.auth.send_sms_func import sent_sms_base
from common.product.models import File, Product, Category, Uom
from common.product.models import SubCategory
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
    files = File.objects.all()
    files.delete()
    products = Product.objects.all()
    products.delete()


@shared_task(name='createProducts')
def createProducts(file_id):
    newProducts = []
    updateProducts = []
    file = File.objects.filter(id=file_id).first()
    if file is None:
        return {'error': "File does not exists"}
    try:
        dataset = Dataset()
        imported_data = dataset.load(file.file.read(), format='xlsx')
    except Exception as e:
        file.delete()
        return {'error': str(e)}
    for data in imported_data:
        # print(data)
        # category, created = Category.objects.get_or_create(title=data[6], title_ru=data[7])
        # if data[10] and data[11]:
        #     t1 = data[10].strip()
        #     t2 = data[11].strip()
        #     top_category, created = Category.objects.get_or_create(title=t1, title_ru=t2)
        try:
            title = data[1]
            code = data[2]
            price = data[5]
            quantity = data[8] or 0
            uom = data[9] or None

            if price:
                price = str(price).replace(',', '')

            if code is None or title is None or bool(re.search(r'[a-zA-Zа-яА-Я]', price)):
                continue

            product = Product.objects.filter(code=code).first()

            if uom:
                uom, created = Uom.objects.get_or_create(title=uom)

            title = title.strip()
            if product:
                updateProducts.append(Product(
                    id=product.id,
                    code=product.code,
                    title=title,
                    price=price,
                    quantity=quantity,
                    uom=uom
                ))
            else:
                newProducts.append(Product(
                    code=code,
                    title=title,
                    price=price,
                    quantity=quantity,
                    uom=uom
                ))
        except Exception as e:
            print(f"Error: {e}")
            continue
    if newProducts:
        Product.objects.bulk_create(newProducts)
    if updateProducts:
        Product.objects.bulk_update(updateProducts, fields=['code', 'title', 'price', 'quantity', 'uom'])
    return {"message": "Product has updated and created successfully"}


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
