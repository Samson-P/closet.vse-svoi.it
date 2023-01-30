import datetime
import os

from django.shortcuts import render, redirect
from django.template.defaulttags import register
from .models import Personnel, Expenses, Log, Notes
from django.http import HttpResponseRedirect

# ORM помощник (client side)
from .forms import *
# from .filters import get_query

# LogIn
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

# ORM запросы
from django.db.models import Q

# Работа с изображениями
from .crop_and_format_img import image_formatting


# Декораторы
@register.filter
def image_url_miniature(path):
    return f"img/png/expenses/{str(path).split('/')[-1]}"


@register.filter
def image_url(path):
    return f"img/jpeg/expenses/{str(path).split('/')[-1].split('.')[0]}.jpeg"


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
def refactor_expenses(request, expenses_id=None):
    # GET запрос
    if request.method == 'GET':
        # Если expenses_id не пустой, вытаскиваем объект класса
        if expenses_id is not None:
            expense = Expenses.objects.get(pk=expenses_id)
            form = ExistsExpensesForm(instance=expense)
            meta = "VIEW"
        # Если expenses_id пустой
        else:
            expense = None
            form = ExpensesForm()
            meta = "CHOICE"

    # POST запрос
    if request.method == 'POST':
        # Если пост запрос со страницы /crm/expenses, то достаем из БД выбранную запись
        if 'show' in request.POST:
            expenses_id = request.POST['expenses']
            return redirect(f'/crm/expenses-{expenses_id}')
        # Если пост запрос на редактирование, то достаем из БД выбранную запись и заполняем ей форму
        elif 'refactor' in request.POST:
            expense = Expenses.objects.get(pk=expenses_id)

            class form(object):
                form_image = RefactorExpensesImageForm
                form_date = RefactorExpensesDataForm(instance=expense)
            expense = None
            meta = "EDITING"
        # Если пост запрос на применение изменений, то сохраняем и достаем из БД измененную запись
        elif 'apply-image' in request.POST:
            form = RefactorExpensesImageForm(request.POST, request.FILES)
            if form.is_valid():
                expense = Expenses.objects.get(pk=expenses_id)
                # Обновляем фото в БД (почитать подробно можно в модуле crop_and_format_img в комментариях)
                expense.image = image_formatting(POST_FILES=request.FILES['file'], pre_name=expense.short_name)
                expense.save()

                return redirect(f'/crm/expenses-{expenses_id}')
            else:
                expense = None
                meta = "EDITING"
        elif 'apply-data' in request.POST:
            form = RefactorExpensesDataForm(request.POST)
            print('Hello')
            if form.is_valid():
                print('Hello')
                expense = Expenses.objects.get(pk=expenses_id)
                expense.short_name = request.POST['short_name']
                expense.name = request.POST['name']
                expense.quantity = request.POST['quantity']
                expense.save()

                return redirect(f'/crm/expenses-{expenses_id}')
            else:
                expense = None
                meta = "EDITING"

    # формируем список для страницы
    context = {'expense': expense, 'form': form, 'meta': meta, 'err': None}

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
    if request.user.is_authenticated:   # Страница откроется только авторизованному пользователю
        err = None
        if request.method == "POST":    # Со стороны клиента было отправлено сообщение
            if len(request.POST['send-message']) != 0:  # Если оно не пустое, обрабатываем
                form = AddNoteForm(request.POST)
                if form.is_valid():     # Если форма валидна, заполняем поля как следует
                    id_creator = Personnel.objects.get(user=request.user)

                    if request.POST['id_expenses'] == '':
                        expense_id = None
                    else:
                        expense_id = Expenses.objects.get(pk=request.POST['id_expenses'])

                    note = Notes.objects.create(
                        creator_id=id_creator, status=request.POST['status'],
                        description=request.POST['send-message'],
                        id_expenses=expense_id
                    )
                    note.save()
                else:
                    pass
            else:   # Если оно пустое, отправляем alert
                err = "Сообщение не должно быть пустым ;)"

        # Логика страницы: форма и данные
        form = AddNoteForm()
        notice = Notes.objects.all()

        if len(notice) == 0:    # Если заметок пока нет, показываем красивое предложение начать
            notice = None

        context = {'notes': notice, 'form': form, 'err': err}
        return render(request, 'notes.html', context)
    else:
        return redirect('/login_page')


def settings(request):
    return render(request, 'settings.html')
