from django.core.validators import MaxValueValidator
from django.db import models

# Create your models here.

class Person(models.Model):
    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    description = models.TextField(default='', blank=True)


class Adress(models.Model):
    city = models.CharField(max_length=64)
    street = models.CharField(max_length=64)
    street_number = models.IntegerField()
    local_number = models.IntegerField(null=True)
    person = models.ForeignKey(Person, null=True, on_delete=models.CASCADE)



class Phone(models.Model):
    phone_number = models.PositiveIntegerField(validators=[MaxValueValidator(999999999)])

    PHONE_CHOICES = (
        (0, 'niezdefiniowany'),
        (1, 'domowy'),
        (2, 'komorkowy'),
        (3, 'sluzbowy')
    )

    phone_type = models.IntegerField(choices=PHONE_CHOICES, default=0)
    phone_person = models.ForeignKey(Person, null=True, on_delete=models.CASCADE)

class Email(models.Model):
    email_adress = models.CharField(max_length=64)

    EMAIL_CHOICES = (
        (0, 'niezdefiniowany'),
        (1, 'domowy'),
        (2, 'sluzbowy')
    )

    email_type = models.IntegerField(choices=EMAIL_CHOICES, default=0)
    email_person = models.ForeignKey(Person, null=True, on_delete=models.CASCADE)

class Group(models.Model):
    group_name = models.CharField(max_length=64)
    group_member = models.ManyToManyField(Person, null=True)

