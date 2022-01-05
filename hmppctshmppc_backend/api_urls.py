from django.urls import path, include

urlpatterns = [
    path('', include('core_api.urls')),
    path('ekatagp/', include('ekatagp.urls'))
]
