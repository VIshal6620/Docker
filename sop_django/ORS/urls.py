from django.urls import path

from . import views

urlpatterns = [
    path('',views.index),
    path('auth/<page>/',views.auth),
    path('<page>/', views.actionId),
    path('<page>/<operation>/<int:id>',views.actionId),
    path('<page>/',views.actionId),


 ]