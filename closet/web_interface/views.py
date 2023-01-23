# Create your views here.
import datetime

from django.shortcuts import render
from django.template.defaulttags import register
from .models import Personnel, Expenses, Log, Notes

# ORM помощник (client side)
# from .forms import TaskAddForm, GanttFilterForm, AddMoreForm
# from .filters import get_query

# LogIn
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import HttpResponseRedirect

# ORM запросы
from django.db.models import Q


# Декораторы
@register.filter
def link_creator(path):
    return f"img/png/expenses/{str(path).split('/')[-1]}"


# Страница авторизации
def login_page(request):
    # формируем список для страницы
    context = {'filters': "", 'err': None}

    return render(request, 'login_page.html', context)


# Страница с ошибкой
def error_page(request):
    return render(request, 'error_page.html')


# Начальная\Главная страница
def main(request):
    # Логика работы фильтров
    expenses = Expenses.objects.all()

    # формируем список для страницы
    context = {'expenses': expenses, 'search': None, 'err': None}

    return render(request, 'main.html', context)


# Страница добавления расходника (новой записи в БД)
def add_expenses(request):
    # Логика работы фильтров
    # tasks, filters = crm_task_filter(request)

    # формируем список для страницы
    context = {'tasks': "", 'filters': "", 'err': None}

    return render(request, 'add_expenses.html', context)


# Страница просмотра/изменения расходника (чтение/редактирование записи в БД)
def refactor_expenses(request):
    # Логика работы фильтров
    # tasks, filters = crm_task_filter(request)

    # формируем список для страницы
    context = {'tasks': "", 'filters': "", 'err': None}

    return render(request, 'refactor_expenses.html', context)


# Страница просмотра/изменения аккаунта (чтение/редактирование записи в БД)
def account(request):
    # Логика работы фильтров
    # tasks, filters = crm_task_filter(request)

    # формируем список для страницы
    context = {'tasks': "", 'filters': "", 'err': None}

    return render(request, 'account.html', context)


# Журнал
def log(request):
    return render(request, 'log.html')


# Заметки
def notes(request):
    return render(request, 'notes.html')


def settings(request):
    return render(request, 'settings.html')
