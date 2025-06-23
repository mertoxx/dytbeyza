# success_stories/forms.py

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML
from .models import SuccessStoryComment

class SuccessStoryCommentForm(forms.ModelForm):
    """Başarı hikayesi yorum formu"""
    
    class Meta:
        model = SuccessStoryComment
        fields = ['name', 'email', 'comment']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Adınız Soyadınız'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'E-posta adresiniz'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Bu başarı hikayesi hakkındaki yorumunuz...'
            }),
        }
        labels = {
            'name': 'Ad Soyad',
            'email': 'E-posta',
            'comment': 'Yorumunuz',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            HTML('<div class="card">'),
            HTML('<div class="card-header"><h5 class="mb-0">Yorum Bırakın</h5></div>'),
            HTML('<div class="card-body">'),
            Row(
                Column('name', css_class='form-group col-md-6 mb-3'),
                Column('email', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Row(
                Column('comment', css_class='form-group col-md-12 mb-3'),
                css_class='form-row'
            ),
            HTML('<div class="text-center">'),
            Submit('submit', 'Yorum Gönder', css_class='btn btn-primary btn-lg px-4'),
            HTML('</div>'),
            HTML('</div>'),
            HTML('</div>'),
        )
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 2:
            raise forms.ValidationError('İsim en az 2 karakter olmalıdır.')
        return name
    
    def clean_comment(self):
        comment = self.cleaned_data.get('comment')
        if len(comment) < 10:
            raise forms.ValidationError('Yorum en az 10 karakter olmalıdır.')
        return comment

class StoryFilterForm(forms.Form):
    """Başarı hikayesi filtreleme formu"""
    
    GENDER_CHOICES = [
        ('', 'Tüm Cinsiyetler'),
        ('male', 'Erkek'),
        ('female', 'Kadın'),
    ]
    
    AGE_RANGE_CHOICES = [
        ('', 'Tüm Yaş Grupları'),
        ('18-25', '18-25 yaş'),
        ('26-35', '26-35 yaş'),
        ('36-45', '36-45 yaş'),
        ('46-55', '46-55 yaş'),
        ('56+', '56+ yaş'),
    ]
    
    SORT_CHOICES = [
        ('-success_date', 'En Yeni'),
        ('success_date', 'En Eski'),
        ('-weight_lost', 'En Çok Kilo Verme'),
        ('weight_lost', 'En Az Kilo Verme'),
        ('duration_months', 'En Kısa Süre'),
        ('-duration_months', 'En Uzun Süre'),
        ('-views', 'En Popüler'),
    ]
    
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control form-control-sm'
        }),
        label='Cinsiyet'
    )
    
    age_range = forms.ChoiceField(
        choices=AGE_RANGE_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control form-control-sm'
        }),
        label='Yaş Grubu'
    )
    
    min_weight_loss = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Min. kg',
            'step': '0.1'
        }),
        label='Min. Kilo Kaybı'
    )
    
    max_duration = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Max ay'
        }),
        label='Max. Süre (ay)'
    )
    
    sort_by = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control form-control-sm'
        }),
        label='Sıralama',
        initial='-success_date'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.form_class = 'filter-form'
        self.helper.layout = Layout(
            HTML('<div class="card mb-4">'),
            HTML('<div class="card-header"><h6 class="mb-0"><i class="fas fa-filter me-2"></i>Filtrele</h6></div>'),
            HTML('<div class="card-body">'),
            Row(
                Column('gender', css_class='col-md-2'),
                Column('age_range', css_class='col-md-2'),
                Column('min_weight_loss', css_class='col-md-2'),
                Column('max_duration', css_class='col-md-2'),
                Column('sort_by', css_class='col-md-2'),
                Column(
                    HTML('<button type="submit" class="btn btn-primary btn-sm w-100 mt-4">Filtrele</button>'),
                    css_class='col-md-2'
                ),
            ),
            HTML('</div>'),
            HTML('</div>'),
        )