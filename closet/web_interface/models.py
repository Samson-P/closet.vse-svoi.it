from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Кадры, Расходные материалы, Журнал перемещения материалов, Заметки


class Personnel(models.Model):
    # Логин и пароль пользователя
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True) # Расширяем модель персонала

    # Контактные данные
    telephone = models.CharField(max_length=11, verbose_name="Номер телефона", blank=True, null=True)
    email = models.CharField(max_length=32, verbose_name="Почтовый ящик", blank=True, null=True)
    discord = models.CharField(max_length=32, verbose_name="Дискорд аккаунт", blank=True, null=True)

    # Личные данные
    image = models.ImageField(verbose_name="Фотография", blank=True, null=True, upload_to="web_interface/static/img/png/avatars")
    personal_information = models.CharField(max_length=512, verbose_name="Личная информация", blank=True, null=True)
    social_media_status = models.CharField(max_length=16, verbose_name="Статус", blank=True, null=True)

    # Кадровые данные
    last_name = models.CharField(max_length=16, verbose_name="Фамилия")
    first_name = models.CharField(max_length=16, verbose_name="Имя")
    position = models.CharField(max_length=32, verbose_name="Должность")
    last_visit = models.DateTimeField(verbose_name="Последнее посещение", auto_now_add=True)
    created_dt = models.DateTimeField(verbose_name="Создание аккаунта", auto_now_add=True)

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class Expenses(models.Model):
    # Короткое наименование для логирования
    short_name = models.CharField(max_length=32, verbose_name="Короткое название расходного материала")
    # Наименование для описания материала
    name = models.TextField(max_length=128, verbose_name="Наименование расходного материала (развернуто)")
    # Количество в штуках или метрах
    quantity = models.CharField(max_length=8, verbose_name="Количество (шт/м)")
    # Изображение расходного материала
    image = models.ImageField(verbose_name="Фотография", upload_to="web_interface/static/img/png/expenses")

    def __str__(self):
        return self.short_name


class Log(models.Model):
    STATUS = (
        ('РАСХОД', 'Потратил на выезд'),
        ('ЗАКУПКА', 'Добавил из закупки'),
        ('ИЗМЕНЕНИЕ', 'Внес изменение'),
        ('УДАЛЕНИЕ', 'Удалил'),
    )
    # Дата реализации действия с расходным материалом
    created_dt = models.DateTimeField(verbose_name="Дата", auto_now_add=True)
    # ID кадра, оставившего лог (в клиенте будет отображаться { last_name + first_name })
    creator_id = models.ForeignKey(Personnel, verbose_name="Создатель", on_delete=models.CASCADE)
    # Статус действия по отношению к расходному материалу
    status = models.CharField(max_length=16, verbose_name='Статус', choices=STATUS)
    # Номер заявки в мониторинге mantis
    task_url = models.CharField(max_length=7, verbose_name="Номер задачи mantis")
    # ID расходного материала (в клиенте будет отображаться полное наименование { name })
    id_expenses = models.ForeignKey(Expenses, verbose_name="Расходник", on_delete=models.CASCADE)
    # Количество в штуках или метрах
    quantity = models.CharField(max_length=8, verbose_name="Количество (шт/м)")

    # Описание действия в клиентской части приложения будет создаваться на основании всех выше перечисленных данных
    # Дата, Номер заявки (если это РАСХОД), Фамилия Имя, Количество, Полное наименование расходника

    def __str__(self):
        return f'{self.created_dt} {self.created_dt} {self.status}'


class Notes(models.Model):
    STATUS = (
        ('TASK', 'Нужно выполнить следующее'),
        ('INVITE', 'Оповещение для своих'),
    )

    # Дата регистрации заметки
    created_dt = models.DateTimeField(verbose_name="Дата", auto_now_add=True)
    # ID кадра, оставившего сообщение (в клиенте будет отображаться { last_name + first_name })
    creator_id = models.ForeignKey(Personnel, verbose_name="Отправитель", on_delete=models.CASCADE)
    # Статус: пишем, что надо что-то сделать (TASK = Задание); что мы (планируем) сделали(-ть) (INVITE = Сообщение)
    status = models.CharField(max_length=16, verbose_name='Статус', choices=STATUS)
    # Содержание
    description = models.CharField(max_length=512, verbose_name="Содержание")
    # ID расходного материала (в клиенте будет отображаться полное наименование { name })
    # Введено для удобства (можно не заполнять)
    id_expenses = models.ForeignKey(Expenses, verbose_name="Расходник", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.creator_id} {self.status} {self.id_expenses}'
