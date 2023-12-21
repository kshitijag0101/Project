from django import forms
from django.core.exceptions import ValidationError
from datetime import datetime


class importFile(forms.Form):
    file = forms.FileField(label='Select Excel File')
    category = forms.ChoiceField(choices=[('Indian', 'Indian'), ('LLP', 'LLP'), ('Foreign', 'Foreign')],
                                 label='Select category')
    month = forms.ChoiceField(choices=[
        ('January', 'January'), ('February', 'February'), ('March', 'March'),
        ('April', 'April'), ('May', 'May'), ('June', 'June'),
        ('July', 'July'), ('August', 'August'), ('September', 'September'),
        ('October', 'October'), ('November', 'November'), ('December', 'December')
    ], label='Select month')
    year = forms.IntegerField(label='Enter Year', initial=datetime.now().year)

    def clean_year(self):
        year = self.cleaned_data['year']
        if year < 1900 or year > 2100:
            raise forms.ValidationError('Invalid year.')
        return year


class LoginForm(forms.Form):
    email = forms.EmailField(
        error_messages={'required': 'Email is required.'},
        widget=forms.TextInput(attrs={'placeholder': 'Enter your email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
        error_messages={'required': 'Password is required.'}
    )


class selectCompany(forms.Form):
    company = forms.ChoiceField(choices=[('Indian', 'Indian'), ('LLP', 'LLP'), ('Foreign', 'Foreign')])


class DashboardFile(forms.Form):
    company = forms.MultipleChoiceField(
        choices=[
            ('Indian', 'Indian'),
            ('LLP', 'LLP'),
            ('Foreign', 'Foreign')
        ],
        label='Select company',
        widget=forms.CheckboxSelectMultiple,
        initial=['Indian', 'LLP', 'Foreign']
    )
    month = forms.ChoiceField(initial='All',choices=[('All', 'All'),
        ('January', 'January'), ('February', 'February'), ('March', 'March'),
        ('April', 'April'), ('May', 'May'), ('June', 'June'),
        ('July', 'July'), ('August', 'August'), ('September', 'September'),
        ('October', 'October'), ('November', 'November'), ('December', 'December')
    ], label='Select month')
    year = forms.IntegerField(label='Enter Year', initial=datetime.now().year, required=False)

    def clean_year(self):
        year = self.cleaned_data['year']
        if year != None:
            if year < 1900 or year > 2100:
                raise forms.ValidationError('Invalid year.')
            return year

