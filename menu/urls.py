from django.urls import path
from .views import menu, export_to_type_a

urlpatterns = [
    path('test/', export_to_type_a, name='export_to_type_a'),
    path('', menu, name='menu')

]
