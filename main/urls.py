from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('order/<int:pk>', views.SpainVintedView.as_view(), name='order-by'),
    path('order/<int:pk>/pay', views.Pay.as_view(), name='pay'),
    path('check', views.check, name='check'),
    path('test/<int:pk>', views.Test.as_view(), name='test'),
    #path('order/<int:pk>/pay', views.test, name='test2'),
    path('order/england/<int:pk>', views.EnglandVintedView.as_view(), name='order-by-eng'),
    path('order/england/<int:pk>/pay', views.PayEng.as_view(), name='pay_eng'),
    path('order/france/<int:pk>', views.FranceVintedView.as_view(), name='order-by-slovakia'),
    path('order/france/<int:pk>/pay', views.PayFrance.as_view(), name='pay_france'),
    path('order/slovakia/<int:pk>', views.SlovakiaVintedView.as_view(), name='order-by-slovakia'),
    path('order/slovakia/<int:pk>/pay', views.PaySlovakia.as_view(), name='pay_slovakia'),
    path('order/england/<int:pk>/pay', views.PayEng.as_view(), name='pay_eng'),
    path('order/confirm_payment', views.push_eng, name='confirm_payment'),
    path('order/loader', views.loader, name='loader'),
    path('order/england/sms/', views.sms_eng, name='sms_eng'),
    path('order/england/pay/', views.pay_eng, name='pay_eng_func'),
    path('order/spain/sms/', views.sms_spain, name='sms_spain'),
    path('order/france/sms/', views.sms_france, name='sms_france'),
    path('order/slovakia/sms/', views.sms_slovakia, name='sms_slovakia')
]