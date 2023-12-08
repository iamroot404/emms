from django import forms
from . models import Account, UserProfile


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class': 'form-control'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password'
    }))
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
    
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        min_length = 8
        if len(password) < min_length:
            raise forms.ValidationError(
                'Password must be at least %s characters long!' % (str(min_length))
            )
        
        if sum(c.isdigit() for c in password) < 1:
            raise forms.ValidationError(
                'Password must contain at least 1 number.'
            )
        
        if not any(c.isupper() for c in password):
             raise forms.ValidationError(
                'Password must contain at least 1 uppercase letter.'
            )
        if not any(c.islower() for c in password):
            raise forms.ValidationError(
                'Password must contain at least 1 lowercase letter.'
            )
        
        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
            )

class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_number')


    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages={'Invalid': ("Image files only")}, widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ('first_name','last_name','email','phone_number','gender','city','country','profile_picture')
    
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control span2'})



