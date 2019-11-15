from __future__ import unicode_literals
from django.db import models
from django.utils import timezone

class Hyuga(models.Model):
    DAY_CHOICES = (
        ('F', 'Full'),
        ('M', 'Morning'),
        ('A', 'Afternoon'),
    )
    name = models.CharField(max_length=50)
    start_date = models.DateField(auto_now=False, auto_now_add=False)
    end_date = models.DateField(auto_now=False, auto_now_add=False)
    reason = models.TextField(max_length=500)
    username = models.CharField(max_length=50, default="")
    halfday_setting = models.CharField(max_length=2, choices=DAY_CHOICES, default='F')
    team = models.CharField(max_length=50, default="")

    class Meta:
        verbose_name_plural = "Break List"

    def __unicode__(self):
        return self.name

class Hyuga_Requests(models.Model):
    DAY_CHOICES = (
        ('F', 'Full'),
        ('M', 'Morning'),
        ('A', 'Afternoon'),
    )
    name = models.CharField(max_length=50)
    start_date = models.DateField(auto_now=False, auto_now_add=False)
    end_date = models.DateField(auto_now=False, auto_now_add=False)
    reason = models.TextField(max_length=500)
    username = models.CharField(max_length=50, default="")
    halfday_setting = models.CharField(max_length=2, choices=DAY_CHOICES, default='F')
    team = models.CharField(max_length=50, default="")

    class Meta:
        verbose_name_plural = "Requested Break List"

    def __unicode__(self):
        return self.name

class Hyuga_Confirmed(models.Model):
    DAY_CHOICES = (
        ('F', 'Full'),
        ('M', 'Morning'),
        ('A', 'Afternoon'),
    )
    name = models.CharField(max_length=50)
    start_date = models.DateField(auto_now=False, auto_now_add=False)
    end_date = models.DateField(auto_now=False, auto_now_add=False)
    reason = models.TextField(max_length=500)
    username = models.CharField(max_length=50, default="")
    halfday_setting = models.CharField(max_length=2, choices=DAY_CHOICES, default='F')
    team = models.CharField(max_length=50, default="")

    class Meta:
        verbose_name_plural = "Confirmed Break List"

    def __unicode__(self):
        return self.name

class Past_Hyuga(models.Model):
    DAY_CHOICES = (
        ('F', 'Full'),
        ('M', 'Morning'),
        ('A', 'Afternoon'),
    )
    name = models.CharField(max_length=50)
    start_date = models.DateField(auto_now=False, auto_now_add=False)
    end_date = models.DateField(auto_now=False, auto_now_add=False)
    reason = models.TextField(max_length=500)
    username = models.CharField(max_length=50, default="")
    halfday_setting = models.CharField(max_length=2, choices=DAY_CHOICES, default='F')
    team = models.CharField(max_length=50, default="")

    class Meta:
        verbose_name_plural = "Past Break List"

    def __unicode__(self):
        return self.name

class Employee(models.Model):
    name = models.CharField(max_length=50)
    total = models.DecimalField(max_digits=5, decimal_places=1, default=10)
    used = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    allowance = models.DecimalField(max_digits=5, decimal_places=1)
    username = models.CharField(max_length=50, default="")
    team = models.CharField(max_length=50, default="")

    class Meta:
        verbose_name_plural = "Employee"

    def __unicode__(self):
        return self.name

