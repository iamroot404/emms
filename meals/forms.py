from django.forms import ModelForm
from django import forms
from .models import Meal, Menu, BookingRequest

class MealForm(ModelForm):
    class Meta:
        model = Meal
        fields = ['meal_name', 'image', 'amount']

        

    def __init__(self, *args, **kwargs):
        super(MealForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class MenuForm(ModelForm):
    class Meta:
        model = Menu
        fields = ['meal', 'date']

        widgets = {
            'date':forms.TextInput(attrs={'type':'datetime-local'}),
        }

        

    def __init__(self, *args, **kwargs):
        super(MenuForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})



class BookingRequestForm(ModelForm):
    class Meta:
        model = BookingRequest
        fields = ['menu']

        

    def __init__(self, *args, **kwargs):
        super(BookingRequestForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})