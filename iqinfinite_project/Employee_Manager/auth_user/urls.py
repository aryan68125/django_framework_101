from django.urls import path,include
urlpatterns = [
    path('auth_api/',include(auth_user.urls_api)),
]
