from django.db import models
from django.contrib.auth.models import AbstractUser
from .utils import send_message_to_telegram


# Импортируем необходимые модули
# Создаём модель пользователя, наследуясь от AbstractUser. Добавляем поле "name" типа CharField.
class User(AbstractUser):
    name = models.CharField(verbose_name='Имя', max_length=254, blank=False)

    def __str__(self):
        return self.username


# Создаем модель "Category" с полем "name" типа CharField. Добавляем менеджер объектов.
class Category(models.Model):
    name = models.CharField(max_length=254)
    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


# Создаем модель "Product" с различными полями, такими как название товара, цена, описание, фото, страна производства,
# категория и количество товара в наличии. Добавляем менеджер объектов.
class Product(models.Model):
    name = models.CharField(verbose_name='Название товара', max_length=255)
    # Поле, представляющее название товара. Тип данных CharField.
    price = models.DecimalField(verbose_name='Цена', max_digits=8, decimal_places=2)
    # Поле, представляющее цену товара. Тип данных DecimalField.
    date = models.DateTimeField(verbose_name='Дата обновления', auto_now_add=True)
    # Поле, представляющее дату обновления товара. Тип данных DateTimeField. Значение автоматически устанавливается при создании объекта.
    description = models.TextField(verbose_name='Описание', blank=True)
    # Поле, представляющее описание товара. Тип данных TextField. Может быть пустым.
    image = models.ImageField(verbose_name='Фото товара', upload_to='files/')
    # Поле, представляющее фото товара. Тип данных ImageField. Фотография будет загружена в папку 'files/'.
    country = models.CharField(verbose_name='Страна', max_length=255)
    # Поле, представляющее страну производства товара. Тип данных CharField.
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    # Внешний ключ, связывающий товар с категорией. Указывает на модель Category. При удалении категории, товар будет удален автоматически.
    quantity = models.PositiveIntegerField('Кол-во товара в наличии', default=0)
    # Поле, представляющее количество товара в наличии. Значение по умолчанию - 0.
    objects = models.Manager()

    # Менеджер объектов для модели Product.

    def __str__(self):
        return self.name

    # Метод для строкового представления объекта товара.

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        # verbose_name_plural - для отображения имени моделей во множественном числе в административной панели Django,
        # например, при отображении списка объектов модели.


# Создаем модель "Cart" для хранения товаров в корзине. Включает поля: количество товара, продукт и пользователь.
class Cart(models.Model):
    quantity = models.PositiveIntegerField(verbose_name='Количество товара в наличии', default=0)
    # Поле, представляющее количество товара в наличии в корзине. Значение по умолчанию - 0.
    product = models.ForeignKey('Product', verbose_name='Продукт', on_delete=models.CASCADE)
    # Внешний ключ, связывающий корзину с продуктом. Указывает на модель Product.
    user = models.ForeignKey('User', verbose_name='Пользователь', on_delete=models.CASCADE)
    # Внешний ключ, связывающий корзину с пользователем. Указывает на модель User.
    objects = models.Manager()

    # Менеджер объектов для модели Cart.

    def __str__(self):
        return str(self.product) + " " + str(self.quantity)

    # Метод для строкового представления объекта корзины.

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        # verbose_name_plural - для отображения имени моделей во множественном числе в административной панели Django,
        # например, при отображении списка объектов модели.


class Order(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Подтверждённый'),
        ('new', 'Новый'),
        ('canseled', 'Отменённый')
    ]
    # Определение поля статуса заказа с выбором из предопределенных вариантов

    status = models.CharField(max_length=254, verbose_name='Статус',
                              choices=STATUS_CHOICES, default='new')
    # Поле, представляющее статус заказа с ограничением выбора из списка STATUS_CHOICES

    date = models.DateTimeField(verbose_name='Дата заказа', auto_now_add=True)

    rejectreason = models.TextField(verbose_name='Причина отказа', blank=True)
    # Поле для хранения причины отказа от заказа. Текстовое поле.

    user = models.ForeignKey('User', verbose_name='Пользователя', on_delete=models.CASCADE)
    # Внешний ключ, связывающий заказ с пользователем

    product = models.ManyToManyField('Product', through='ProductInOrder', related_name='order')

    # Многие-ко-многим отношение между заказом и товарами через модель ItemInOrder

    def quantity_product(self):
        quantity_product = 0
        for productinorder in self.productinorder_set.all():
            quantity_product += productinorder.quantity
        return quantity_product

    # Метод для подсчета общего количества товаров в заказе

    def __str__(self):
        return str(self.date.ctime()) + ' | ' + self.user.name() + \
            ' | Количество: ' + str(self.quantity_product())

    # Метод для строкового представления объекта заказа

    def status_verbose(self):
        return dict(self.STATUS_CHOICES)[self.status]

    # Метод для получения текстового представления статуса заказа

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class ProductInOrder(models.Model):
    quantity = models.IntegerField(verbose_name='Количество', blank=False, default=0)
    # Поле, представляющее количество товара в заказе. Тип данных IntegerField. Не может быть пустым.
    order = models.ForeignKey('Order', verbose_name='Заказ', on_delete=models.CASCADE)
    # Внешний ключ, связывающий товар в заказе с заказом. Указывает на модель Order. При удалении заказа, товар в заказе будет удален автоматически.
    product = models.ForeignKey('Product', verbose_name='Товар', on_delete=models.CASCADE)
    # Внешний ключ, связывающий товар в заказе с товаром. Указывает на модель Product. При удалении товара, товар в заказе будет удален автоматически.
    price = models.DecimalField(verbose_name='Стоимость', max_digits=10, decimal_places=2, blank=False, default=0.00)

    # Поле, представляющее стоимость товара в заказе. Тип данных DecimalField. Не может быть пустым.

    def __str__(self):
        return str(self.product) + " " + str(self.quantity) + '(' + str(self.price) + ')'

    # Метод для строкового представления объекта товара в заказе.

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'


class Payment(models.Model):
    name = models.CharField(max_length=100)
    telegram = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    policy = models.BooleanField()

    def __str__(self):
        return self.name

    def save_and_send_to_telegram(self):
        self.save()  # Сохраняем данные в БД
        message = f'Имя: {self.name}\nTelegram: {self.telegram}\nТовар: {self.product.name}\nСогласие с политикой: {self.policy}'

        # Замените 'YOUR_BOT_TOKEN' на токен вашего Telegram бота
        bot_token = '6373170365:AAFuMgN0GWsHNaWX8l6GiaW-X7zguQFvc1Y'

        # Замените 'YOUR_CHAT_ID' на ID чата, куда вы хотите отправить сообщение
        chat_id = '-991872617'

        send_message_to_telegram(message, bot_token, chat_id)  # Отправляем сообщение в Telegram

    class Meta:
        verbose_name = 'Таблица для хранения данных платежей'
        verbose_name_plural = 'Таблицы для хранения данных платежей'
