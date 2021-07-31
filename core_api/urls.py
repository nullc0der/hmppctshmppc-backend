from django.urls import path

from core_api import views

urlpatterns = [
    path('initiatepayment/', views.InitiatePayment.as_view()),
    path('checkpaymentcompleted/', views.CheckPaymentCompleted.as_view()),
    path('getstats/', views.GetStats.as_view())
]
