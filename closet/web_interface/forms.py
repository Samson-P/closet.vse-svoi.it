from .models import Expenses, Log, Notes, TechnicalSupport
from django.forms import Form, ModelForm, ModelMultipleChoiceField, FileField, TextInput, CharField, Textarea


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


class TechnicalSupportForm(ModelForm):

	class Meta:
		model = TechnicalSupport
		fields = ['theme', 'description_of_the_problem', 'logs', 'attachments']
		widgets = {
			'description_of_the_problem': Textarea(attrs={'rows': "4", 'cols': "50", 'title': 'Опишите проблему'}),
			'logs': Textarea(attrs={'rows': "8", 'cols': "50", 'title': 'Введите логи, если такие имеются'}),
		}
