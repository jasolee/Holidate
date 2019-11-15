# tutorial/tables.py
import django_tables2 as tables
from django_tables2.columns import TemplateColumn

from .models import Hyuga_Requests

class CheckBoxColumnWithName(tables.CheckBoxColumn):

    def header(self):
        return self.verbose_name

class HyugaRequestTable(tables.Table):
	selection = CheckBoxColumnWithName(verbose_name="Select" , accessor="pk")

	class Meta:
		model = Hyuga_Requests
		attrs = {'class': 'paleblue'}