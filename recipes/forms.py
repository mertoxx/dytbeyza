from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from .models import RecipeRating

class RecipeRatingForm(forms.ModelForm):
    """Tarif değerlendirme formu"""
    
    class Meta:
        model = RecipeRating
        fields = ['name', 'email', 'rating', 'comment']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Adınız'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'E-posta adresiniz'
            }),
            'rating': forms.Select(attrs={
                'class': 'form-control'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tarif hakkındaki yorumunuz...'
            }),
        }
        labels = {
            'name': 'Ad Soyad',
            'email': 'E-posta',
            'rating': 'Puanınız',
            'comment': 'Yorumunuz',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-3'),
                Column('email', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('rating', css_class='form-group col-md-12 mb-3'),
            ),
            'comment',
            Submit('submit', 'Yorum Gönder', css_class='btn btn-primary mt-3')
        )