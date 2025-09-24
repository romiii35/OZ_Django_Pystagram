from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import FormView

User = get_user_model()


class SignupForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # class_update_fields = ('password1', 'password2')
        # class_default_fields = ('password1', 'password2')
        for field in ('password1', 'password2'):
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['placeholder'] = 'password '
            if field == 'password1':
                self.fields[field].label = '비밀번호'
            else:
                self.fields[field].label = '비밀번호 확인'


    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'nickname')
        labels = {
            'email': '이메일',
            'nickname' : '닉네임'
        }

        widgets = {
            'email' : forms.EmailInput(
                attrs={
                    'placeholder':'example@example.com',
                    'class':'form-control'
                }
            ),
            'nickname' : forms.TextInput(
                attrs={
                    'placeholder' : '닉네임',
                    'class' : 'form-control'
                }
            )
        }

class LoginForm(forms.Form):
    # Modelform은 save 할때, user가 저장이 되니까,,,이번에는 'Form'을 사용
    # 'ModelForm'은 field를 안채워도 되는데, 'Form'은 field를 넣어야한다.
    email = forms.CharField(
        label = '이메일',
        required = True,
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'example.com',
                'class': 'form-control'
            }
        )
    )
    password = forms.CharField(
        label='패스워드',
        required = True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'PASSWORD',
                'class': 'form-control'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None


    def clean(self):
        # clean = is_valid
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        self.user = authenticate(email=email, password=password)

        if not self.user.is_active:
            raise forms.ValidationError('유저가 인증되지 않았습니다.')
        return cleaned_data

