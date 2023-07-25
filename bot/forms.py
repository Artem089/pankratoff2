# forms.py
from django import forms
from .models import Payment
from .utils import send_message_to_telegram


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['name', 'telegram', 'product', 'policy']

    def save_and_send_to_telegram(self):
        payment = super().save()  # Сохраняем данные формы в БД

        # Отправляем данные в телеграмм, используя функцию send_message_to_telegram
        name = self.cleaned_data['name']
        telegram = self.cleaned_data['telegram']
        product = self.cleaned_data['product']
        message = f"Пользователь {name} (@{telegram}) выбрал товар: {product}."

        # Замените 'YOUR_BOT_TOKEN' на токен вашего Telegram бота
        bot_token = '6373170365:AAFuMgN0GWsHNaWX8l6GiaW-X7zguQFvc1Y'

        # Замените 'YOUR_CHAT_ID' на ID чата, куда вы хотите отправить сообщение
        chat_id = '-991872617'

        send_message_to_telegram(message, bot_token, chat_id)  # Отправить сообщение в телеграм

        return payment
