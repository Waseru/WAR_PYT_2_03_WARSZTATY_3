from django.shortcuts import render, render_to_response
from django.views import View
from kontakty.models import Adress, Person, Email, Phone, Group

# Create your views here.

class ContactList(View):
    def get(self, request):

        contact_list = Person.objects.all().order_by('name')
        return render_to_response('contact_list.html', {
            'contact_list': contact_list
        })
    def post(self, request ):
        pass

class ModifyContact(View):
    pass