from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import User

class RegisterForm(UserCreationForm):
    full_name = forms.CharField(max_length=100, required=True, label='نام کامل')
    phone = forms.CharField(max_length=11, required=True, label='شماره موبایل')
    email = forms.EmailField(required=False, label='ایمیل')
    address = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3}), label='آدرس')
    postal_code = forms.CharField(max_length=10, required=False, label='کد پستی')

    class Meta:
        model = User
        fields = ['full_name', 'phone', 'email', 'password1', 'password2', 'address', 'postal_code']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError('این شماره موبایل قبلاً ثبت شده است.')
        return phone


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'email', 'address', 'postal_code']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3, 'placeholder': 'آدرس خود را وارد کنید'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.exclude(id=self.instance.id).filter(email=email).exists():
            raise forms.ValidationError('این ایمیل قبلاً ثبت شده است.')
        return email


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'placeholder': self.fields[field].label
            })