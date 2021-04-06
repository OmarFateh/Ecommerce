from django import forms
# from django.contrib.auth import password_validation
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, PasswordChangeForm


User = get_user_model()

class AddUserForm(forms.ModelForm):
    """
    User creation form class.
    """
    first_name = forms.CharField(
        label='',
        max_length=55, 
        widget=forms.TextInput(attrs={'class':'form-control', 'name':'firstname', 'required':True}),
    )
    last_name = forms.CharField(
        label='',
        max_length=55, 
        widget=forms.TextInput(attrs={'class':'form-control', 'name':'lastname', 'required':True}),
    )
    email = forms.EmailField(
        label='',
        max_length=60, 
        widget=forms.EmailInput(attrs={'class':'form-control js-validate-email', 'name':'email', 'required':True}),
    )
    email2 = forms.EmailField(
        label='',
        max_length=60, 
        widget=forms.EmailInput(attrs={'class':'form-control js-validate-email2', 'name':'confirm_email', 'required':True}),
    )
    password1 = forms.CharField(
        label='',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control js-validate-password1', 'required':True}),
    )
    password2 = forms.CharField(
        label='',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control js-validate-password2', 'required':True}),
    )

    class Meta:
        model   = User
        fields  = ['first_name', 'last_name', 'email', 'email2', 'password1', 'password2']    

    def clean_email2(self):
        """
        Validate emails.
        """
        email1 = self.cleaned_data.get("email")
        email2 = self.cleaned_data.get('email2') 
        # check if the two emails match.
        if email1 != email2:
            raise forms.ValidationError('The two email fields didn’t match.')
        # check if the email has already been used.  
        if User.objects.filter(email__iexact=email2).exists():
            raise forms.ValidationError("An account with this Email already exists.")
        return email2

    def clean_password2(self):
        """
        Validate passwords.
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get('password2') 
        # check if the two passwords match.
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError('The two password fields didn’t match.')
        return password2

class UpdateUserForm(forms.ModelForm):
    """
    Update User model form.
    """
    first_name = forms.CharField(
        label='First name',
        max_length=55, 
        widget=forms.TextInput(attrs={'class':'form-control', 'name':'first_name', 'required':True}),
    )
    last_name = forms.CharField(
        label='Last name',
        max_length=55, 
        widget=forms.TextInput(attrs={'class':'form-control', 'name':'last_name', 'required':True}),
    )
    email = forms.EmailField(
        label='Email address',
        max_length=60, 
        widget=forms.EmailInput(attrs={'class':'form-control js-validate-email', 'name':'email', 'required':True}),
    )

    class Meta:
        model  = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(UpdateUserForm, self).__init__(*args, **kwargs)    

    def clean_email(self):
        """
        Validate email.
        """
        email = self.cleaned_data.get("email")
        # check if the email has already been used.   
        if User.objects.filter(email__iexact=email).exclude(email__iexact=self.request.user.email).exists():
            raise forms.ValidationError("An account with this Email already exists.")
        return email

class EmailValidationOnForgotPassword(PasswordResetForm):
    """
    Override password reset form email field and its validation.
    """
    email = forms.EmailField(
        label='',
        max_length=255,
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class':'form-control', 'name':'email', 'required': True})
    )

    def clean_email(self):
        """
        Validate email.
        """
        # fetch entered email.
        email = self.cleaned_data['email']
        # check if the entered email doesn't exist.
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise forms.ValidationError("Your email was entered incorrectly. Please enter it again.")
        return email


class PasswordFieldsOnForgotPassword(SetPasswordForm):
    """
    Override set password form password fields.
    """
    new_password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control js-validate-password1 mb-2', 'required':True}),
        strip=False,
        # help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label='',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control js-validate-password2', 'required':True}),
    )


class PasswordFieldsOnChangePassword(PasswordChangeForm):
    """
    Override password change form password fields.
    """
    old_password = forms.CharField(
        label='',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True, 'class':'form-control mb-2', 'required':True}),
    )
    new_password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control js-validate-password1 mb-2', 'required':True}),
        strip=False,
        # help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label='',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control js-validate-password2', 'required':True}),
    )
