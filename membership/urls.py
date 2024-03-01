from django.urls import path
from .views import *

urlpatterns = [
    path('', home),
    path('form/', calculate_date),
    path('delete/<int:id>', delete),
    path('delete_user/<int:id>', delete_user),
    path('delete_member_check/<int:id>', delete_member_check),
    path('edit/<int:id>', edit),
    path('search/', search),
    path('search_results/', search_results),
    path('search_results_member/', search_results_member),
    path('user_form/' ,user),
    path('check/', check),
    path('check_member/', check_member),
    path('check_in/<int:reg_id>/', check_in , name='check_in'),
    path('remain/<int:id>', remain),
]