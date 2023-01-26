from .models import Expenses
from django.forms import Form, ModelForm, ModelMultipleChoiceField, FileField, ImageField


# Форма для выбора конкретной позиции из БД на странице редактирования расходников
class expenses_form(Form):
	# ...

	expenses = ModelMultipleChoiceField(
		queryset=Expenses.objects.all(), label=''
	)


class exists_expenses_form(ModelForm):
	# Форма для редактирования записи расходника

	class Meta:
		model = Expenses
		fields = "__all__"


class refactor_expenses_form(ModelForm):
	# Форма для редактирования записи расходника
	file = FileField()

	class Meta:
		model = Expenses
		fields = ['short_name', 'name', 'quantity']

