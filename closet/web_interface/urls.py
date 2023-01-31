from django.urls import path
from . import views


urlpatterns = [
    path('login_page/', views.login_page),
    path('error', views.error_page),
    path('', views.main),
    path('main', views.main),
    path('crm/expenses-<int:expenses_id>', views.refactor_expenses),
    path('crm/expenses', views.refactor_expenses),
    path('crm/add_expenses', views.add_expenses),
    path('account/@<str:signa>', views.account),
    path('log', views.log),
    path('notes', views.notes),
    path('settings', views.settings),
    path('support', views.support),
]
