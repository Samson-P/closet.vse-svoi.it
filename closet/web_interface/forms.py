from .models import Expenses, Log, Notes
from django.forms import Form, ModelForm, ModelMultipleChoiceField, FileField, ImageField


# Форма для выбора конкретной позиции из БД на странице редактирования расходников
class ExpensesForm(Form):
	# ...

	expenses = ModelMultipleChoiceField(
		queryset=Expenses.objects.all(), label=''
	)


class ExistsExpensesForm(ModelForm):
	# Форма для редактирования записи расходника

	class Meta:
		model = Expenses
		fields = "__all__"


class RefactorExpensesImageForm(Form):
	# Форма для редактирования записи расходника
	file = FileField()


class RefactorExpensesDataForm(ModelForm):
	class Meta:
		model = Expenses
		fields = ['short_name', 'name', 'quantity']


class AddNoteForm(ModelForm):
	class Meta:
		model = Notes
		fields = ['status', 'id_expenses']
