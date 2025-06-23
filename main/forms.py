# main/forms.py

from django import forms
from django.utils import timezone
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    """İletişim formu"""
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Adınız Soyadınız'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'E-posta Adresiniz'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Konu'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Mesajınız...'
            }),
        }
        labels = {
            'name': 'Ad Soyad',
            'email': 'E-posta',
            'subject': 'Konu',
            'message': 'Mesaj',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-3'),
                Column('email', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Row(
                Column('subject', css_class='form-group col-md-12 mb-3'),
                css_class='form-row'
            ),
            Row(
                Column('message', css_class='form-group col-md-12 mb-3'),
                css_class='form-row'
            ),
            Submit('submit', 'Mesaj Gönder', css_class='btn btn-primary btn-lg')
        )

class NewsletterForm(forms.Form):
    """Newsletter kayıt formu"""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'E-posta adresiniz...'
        }),
        label='E-posta'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.field_template = 'bootstrap4/layout/inline_field.html'
        self.helper.layout = Layout(
            'email',
            Submit('submit', 'Abone Ol', css_class='btn btn-primary ml-2')
        )