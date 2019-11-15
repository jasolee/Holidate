from django.shortcuts import render
from django.template.response import TemplateResponse
from django.views.generic import TemplateView
from django import forms
from django.core.context_processors import csrf
from django.contrib import messages
from django_tables2 import RequestConfig
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.models import User


from datetime import datetime
from decimal import Decimal
from itertools import chain
from operator import attrgetter

from .forms import HyugaRequestForm
from .tables import HyugaRequestTable
from .models import Employee, Hyuga, Hyuga_Requests, Past_Hyuga, Hyuga_Confirmed

sender_email = 'info@coinplug.com'
admin_email = 'dylee.080606@gmail.com'


def isoverlapped(d1,d2,d3,d4,hds1,hds2):
    assert(d1 <= d2 and d3 <= d4)
    if hds1 == 'F' and hds2 == 'F':
        if (d1 < d3 and d2 < d4) or (d4 < d1 and d4 < d2):
            return False
        else: return True
    elif hds1 == 'F' and (hds2 == 'M' or hds2 == 'A'):
        assert(d3 == d4)
        if d1 <= d3 and d3 <= d2:
            return True
        else: return Falseim
    elif (hds1 == 'M' or hds1 == 'A') and hds2 == 'F':
        assert(d1 == d2)
        if d3 <= d1 and d1 <= d4:
            return True
        else: return False
    else:
        assert(d1 == d2 and d3 == d4)
        if d1 == d3:
            if hds1 == hds2:
                return True
            else: return False
        else:
            return False

def mainpage(request):

    if request.user.is_authenticated() == False:
        return HttpResponseRedirect("/Login/")

    break_data = Hyuga.objects.all()
    emp_data = Employee.objects.all()
    past_break_data = Past_Hyuga.objects.all()
    request_data = Hyuga_Requests.objects.all()
    confirmed_data = Hyuga_Confirmed.objects.all()
    pending_data = sorted(chain(request_data, confirmed_data), key=attrgetter('start_date'))
    self_data = emp_data.get(username=request.user.username)

    for query in break_data:
        if query.end_date < datetime.today().date():
            Past_Hyuga.objects.create(name=query.name, start_date=query.start_date, end_date=query.end_date, reason=query.reason, username=query.username, halfday_setting=query.halfday_setting, team=query.team)

    if request.method == "POST":
        f = HyugaRequestForm(request.POST)
        if f.is_valid():
            halfday_setting = f.cleaned_data['halfday_setting']
            start_date = f.cleaned_data['start_date']
            if halfday_setting == 'F':
                end_date = f.cleaned_data['end_date']
            else:
                end_date = start_date
            reason = f.cleaned_data['reason']
            current_emp = Employee.objects.get(username=request.user.username)
            requested_duration = Decimal((end_date - start_date).days) + Decimal(1.0)

            if start_date <= end_date and end_date < datetime.today().date():
                messages.error(request, 'You have registered a break in the past...')
                return render(request, 'timeline/mainpage_2.html', {
                        'form': f,
                        'emp_data': emp_data,
                        'break_data': break_data,
                        'past_break_data': past_break_data,
                        'self_data': self_data
                    })

            if halfday_setting != 'F':
                if requested_duration == 1:
                    requested_duration = 0.5
                else:
                    messages.error(request,'You must register Morning or Afternoon breaks seperately: Make sure that the start date and end date are the same', fail_silently=True)

                    return render(request, 'timeline/mainpage_2.html', {
                        'form': f,
                        'emp_data': emp_data,
                        'break_data': break_data,
                        'past_break_data': past_break_data,
                        'self_data': self_data
                    })

            if requested_duration < 0.5:
                messages.error(request, 'Invalid break request: Please confirm dates. Requested: ' + str(start_date) + ' ~ ' + str(end_date) + '(' + halfday_setting + ')' +'.')
                return render(request, 'timeline/mainpage_2.html', {
                            'form': f,
                            'emp_data': emp_data,
                            'break_data': break_data,
                            'past_break_data': past_break_data,
                            'self_data': self_data
                        })


            for hyuga in pending_data:
                if hyuga.username == request.user.username:
                    if isoverlapped(hyuga.start_date, hyuga.end_date, start_date, end_date, hyuga.halfday_setting, halfday_setting):
                        messages.error(request, 'Requested break overlaps with existing pending or confirmed breaks. Please check your break dates')
                        return render(request, 'timeline/mainpage_2.html', {
                            'form': f,
                            'emp_data': emp_data,
                            'break_data': break_data,
                            'past_break_data': past_break_data,
                            'self_data': self_data
                        })

            for hyuga in break_data:
                if hyuga.username == request.user.username:
                    if isoverlapped(hyuga.start_date, hyuga.end_date, start_date, end_date, hyuga.halfday_setting, halfday_setting):
                        messages.error(request, 'Requested break overlaps with existing pending or confirmed breaks. Please check your break dates')
                        return render(request, 'timeline/mainpage_2.html', {
                            'form': f,
                            'emp_data': emp_data,
                            'break_data': break_data,
                            'past_break_data': past_break_data,
                            'self_data': self_data
                        })
                    
            if requested_duration <= current_emp.allowance and requested_duration >= 0.5:
                current_emp.used += Decimal(requested_duration)
                current_emp.allowance = current_emp.total - current_emp.used
                current_emp.save()
                name = current_emp.name
                username = current_emp.username
                team = current_emp.team
                Hyuga_Requests.objects.create(name=name, start_date=start_date, end_date=end_date, reason=reason, username=username, halfday_setting=halfday_setting, team=team)
                messages.success(request, 'Break Request for: '+ name + '(' + reason + ')' + '  ' + str(start_date) + ' ~ ' + str(end_date) + '(' + halfday_setting + ')' + ' has been sent.' )

                team_list = Employee.objects.filter(team=team)
                for member in team_list:
                    user = User.objects.get(username=member.username)
                    if user.is_superuser or user.is_staff:
                        staff_email = User.objects.get(username=member.username).email
                        send_mail('Break Request: '+name, 'Break Request for: '+ name + '(' + reason + ')' + '  ' + str(start_date) + ' ~ ' + str(end_date) + '(' + halfday_setting + ')', sender_email, [staff_email], fail_silently=False,)
            else:
                messages.error(request, 'Not enough allowance. Current allowance: ' + str(current_emp.allowance) + ' days. Requested: ' + str(requested_duration) + ' days.')
    else:
        f = HyugaRequestForm()
        args = {}
        args.update(csrf(request))
        args['form'] = f

    return render(request, 'timeline/mainpage_2.html', {
        'form': f,
        'emp_data': emp_data,
        'break_data': break_data,
        'past_break_data': past_break_data,
        'self_data': self_data
    })

def staffsite(request):

    if request.user.is_authenticated() == False:
        return HttpResponseRedirect("/Login/")

    if request.method == 'POST':
        list_of_ids = request.POST.getlist('selection')
        if request.POST.get('delete') == "":
            req_list = Hyuga_Requests.objects.filter(id__in=request.POST.getlist('selection'))
            for req in req_list:
                emp_query = Employee.objects.get(username=req.username)
                delta = req.end_date - req.start_date
                if req.halfday_setting == 'F':
                    emp_query.used -= Decimal(delta.days + 1)
                else:
                    emp_query.used -= Decimal(0.5)
                emp_query.allowance = emp_query.total - emp_query.used
                emp_query.save()
            Hyuga_Requests.objects.filter(id__in=request.POST.getlist('selection')).delete()

        elif request.POST.get('approve') == "":
            req_list = Hyuga_Requests.objects.filter(id__in=request.POST.getlist('selection'))
            for req in req_list:
                Hyuga_Confirmed.objects.create(name=req.name, start_date=req.start_date, end_date=req.end_date, reason=req.reason, username=req.username, halfday_setting=req.halfday_setting, team=req.team)

                send_mail('Break Confirmed: '+ req.name, 'Break Confirmed for: '+ req.name + '(' + req.reason + ')' + '  ' + str(req.start_date) + ' ~ ' + str(req.end_date) + '(' + req.halfday_setting + ')', sender_email, [admin_email], fail_silently=False,)

            Hyuga_Requests.objects.filter(id__in=request.POST.getlist('selection')).delete()

    current_emp = Employee.objects.get(username=request.user.username)
    table = HyugaRequestTable(Hyuga_Requests.objects.filter(team=current_emp.team))
    RequestConfig(request).configure(table)
    return render(request, 'staff_site/staffsite.html', {'table': table})

def profile(request):

    if request.user.is_authenticated() == False:
        return HttpResponseRedirect("/Login/")

    break_data = Hyuga.objects.all()
    emp_data = Employee.objects.all()
    past_break_data = Past_Hyuga.objects.all()
    request_data = Hyuga_Requests.objects.all()
    confirmed_data = Hyuga_Confirmed.objects.all()
    pending_data = sorted(chain(request_data, confirmed_data), key=attrgetter('start_date'))
    self_data = emp_data.get(username=request.user.username)

    if request.user.is_superuser == False:
        if request.user.is_staff:
            for emp in emp_data:
                if emp.username == request.user.username:
                    team = emp.team
            break_data = break_data.filter(team=team)
            emp_data = emp_data.filter(team=team)
            past_break_data = past_break_data.filter(team=team)
            pending_data = sorted(chain(request_data.filter(team=team), confirmed_data.filter(team=team)), key=attrgetter('start_date'))
        else:
            break_data = break_data.filter(username=request.user.username)
            emp_data = emp_data.filter(username=request.user.username)
            past_break_data = past_break_data.filter(username=request.user.username)
            pending_data = sorted(chain(request_data.filter(username=request.user.username), confirmed_data.filter(username=request.user.username)), key=attrgetter('start_date'))

    return render(request, 'timeline/profile.html', {
        'break_data': break_data,
        'past_break_data': past_break_data,
        'pending_data': pending_data,
        'emp_data': emp_data,
        'self_data': self_data
    })