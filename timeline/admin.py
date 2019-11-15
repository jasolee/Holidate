from django.contrib import admin
from decimal import Decimal

from .models import Hyuga, Employee, Past_Hyuga, Hyuga_Requests, Hyuga_Confirmed

from quickstart import createEvent

# Register your models here.

def delete_selected(modeladmin, request, queryset):
	for query in queryset:
		delta = query.end_date - query.start_date
		emp_query = Employee.objects.get(username=query.username)
		if query.halfday_setting == 'F':
			emp_query.used -= Decimal(delta.days + 1)
		else:
			emp_query.used -= Decimal(0.5)
		emp_query.allowance = emp_query.total - emp_query.used
		emp_query.save()
		query.delete()

def clean_delete_selected(modeladmin, request, queryset):
	for query in queryset:
		query.delete()

class HyugaAdmin(admin.ModelAdmin):
    list_display = ('name','start_date','end_date','reason','halfday_setting','team')
    ordering = ['start_date']
    date_hierarchy = 'start_date'
    actions=[delete_selected, clean_delete_selected]


class PastHyugaAdmin(admin.ModelAdmin):
    list_display = ('name','start_date','end_date','reason','halfday_setting','team')
    ordering = ['start_date']
    date_hierarchy = 'start_date'

class EmployeeAdmin(admin.ModelAdmin):
	list_display = ('name', 'total', 'used', 'allowance','team')

def approve_selected(modeladmin, request, queryset):
	for query in queryset:
		Hyuga.objects.create(name=query.name, start_date=query.start_date, end_date=query.end_date, reason=query.reason, username=query.username, halfday_setting=query.halfday_setting, team=query.team)
		createEvent(query.name, query.start_date, query.end_date, query.reason)
		query.delete()

class RequestAdmin(admin.ModelAdmin):
	list_display = ('name','start_date','end_date','reason','halfday_setting','team')
	ordering = ['start_date']
	date_hierarchy = 'start_date'
	# actions=[approve_request]

	# def has_add_permission(self, request):
	# 	return False

class ConfirmedAdmin(admin.ModelAdmin):
	list_display = ('name','start_date','end_date','reason','halfday_setting','team')
	ordering = ['start_date']
	date_hierarchy = 'start_date'
	actions=[approve_selected, delete_selected, clean_delete_selected]

	def has_add_permission(self, request):
		return False


admin.site.register(Hyuga, HyugaAdmin)
admin.site.register(Employee, EmployeeAdmin)
# admin.site.register(Past_Hyuga, PastHyugaAdmin)
# admin.site.register(Hyuga_Requests, RequestAdmin)
admin.site.register(Hyuga_Confirmed, ConfirmedAdmin)
