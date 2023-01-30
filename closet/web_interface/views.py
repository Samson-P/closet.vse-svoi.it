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
from django.contrib.auth import authenticate, login, logout
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
    if request.user.is_authenticated:
        logout(request)
    else:
        if request.method == 'POST':
            # Получаем данные авторизации с формы
            user_login = str(request.POST['loginOfUser'])
            user_password = str(request.POST['passwordOfUser'])

            # try to get user in Db
            user = authenticate(username=user_login, password=user_password)

            # if user exists
            if user is not None:
                # authorize user
                login(request, user)
                return HttpResponseRedirect("/main")
            else:
                # not correct login or password
                return HttpResponseRedirect("/login_page")

    return render(request, 'login_page.html')


# Страница с ошибкой
def error_page(request):
    return render(request, 'error_page.html')


# Начальная\Главная страница
def main(request):
    if request.user.is_authenticated:
        err = None
        if request.method == 'POST':
            # Логика работы FORM
            if str(request.POST['task']).isdigit() and len(str(request.POST['task'])) == 7:
                one_expense = Expenses.objects.get(pk=request.POST['expense'])
                count = int(one_expense.quantity) - int(request.POST['count'])
                if count > 0:
                    status = 'РАСХОД'
                else:
                    status = 'ИЗМЕНЕНИЕ'
                id_creator = Personnel.objects.get(user=request.user).user
                log_line = Log.objects.create(
                    creator_id=id_creator, id_expenses=one_expense,
                    status=status, task_url=request.POST['task'],
                    quantity=abs(count)
                    )
                log_line.save()
                one_expense.quantity = request.POST['count']
                one_expense.save()
            else:
                err = "Введите полностью номер задачи и повторите попытку!"
        expenses = Expenses.objects.all()

        # формируем список для страницы
        context = {'expenses': expenses, 'search': None, 'err': err}

        return render(request, 'main.html', context)
    else:
        return redirect("/login_page")


# Страница добавления расходника (новой записи в БД)
def add_expenses(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            # Форма
            form = ExistsExpensesForm()
        if request.method == 'POST':
            # Заполняем
            expense = Expenses.objects.create()
            form = ExistsExpensesForm(request.POST, request.FILES, instance=expense)
            if form.is_valid():
                form_expense = form.save()
                form_expense.image = image_formatting(POST_FILES=request.FILES['image'], pre_name=expense.short_name)
                form_expense.save()
                return redirect('/main')
        # формируем список для страницы
        context = {'form': form, 'err': None}

        return render(request, 'add_expenses.html', context)
    else:
        return redirect("/login_page")


# Страница просмотра/изменения расходника (чтение/редактирование записи в БД)
def refactor_expenses(request, expenses_id=None):
    if request.user.is_authenticated:
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
                    form_data = RefactorExpensesDataForm(instance=expense)

                meta = "EDITING"
            # Изменение изображения в записи расходника
            elif 'apply-image' in request.POST:
                form = RefactorExpensesImageForm(request.POST, request.FILES)
                if form.is_valid():
                    expense = Expenses.objects.get(pk=expenses_id)
                    # Обновляем фото в БД (почитать подробно можно в модуле crop_and_format_img в комментариях)
                    expense.image = image_formatting(POST_FILES=request.FILES['file'], pre_name=expense.short_name)
                    expense.save()
                    # Смотрим изменения
                    return redirect(f'/crm/expenses-{expenses_id}')
                else:
                    expense = None
                    meta = "EDITING"
            # Изменение текстовых данных в записи расходника
            elif 'apply-data' in request.POST:
                form = RefactorExpensesDataForm(request.POST)
                if form.is_valid():
                    expense = Expenses.objects.get(pk=expenses_id)
                    expense.short_name = request.POST['short_name']
                    expense.name = request.POST['name']
                    expense.quantity = request.POST['quantity']
                    expense.save()

                    return redirect(f'/crm/expenses-{expenses_id}')
                else:
                    expense = None
                    meta = "EDITING"
            # Удаление записи из БД
            elif 'delete' in request.POST:
                expense = Expenses.objects.get(pk=expenses_id)
                try:
                    os.remove(f'{str(expense.image)}')
                except:
                    pass
                expense.delete()
                return redirect(f'/main')

        # формируем список для страницы
        context = {'expense': expense, 'form': form, 'meta': meta, 'err': None}

        return render(request, 'refactor_expenses.html', context)
    else:
        return redirect('/login_page')


# Страница просмотра/изменения аккаунта (чтение/редактирование записи в БД)
def account(request):
    # Логика работы фильтров
    # tasks, filters = crm_task_filter(request)

    # формируем список для страницы
    context = {'tasks': "", 'filters': "", 'err': None}

    return render(request, 'account.html', context)


# Журнал
def log(request):
    if request.user.is_authenticated:
        logs = Log.objects.all()
        return render(request, 'log.html', {'logs': logs})
    else:
        return redirect('/login_page')


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
    if request.user.is_authenticated:
        return render(request, 'settings.html')
    else:
        return redirect('/login_page')
