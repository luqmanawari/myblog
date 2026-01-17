from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class SignUpForm(UserCreationForm):
    """
    Custom signup form extending Django's UserCreationForm
    for user registration with additional fields
    """
    
    
     
    email = forms.EmailField(
        required=True,
      )
    
    username = forms.CharField(
        max_length=150,
        required=True,
      )
    
    password1 = forms.CharField(
        label='Password',
    
    )
    
    password2 = forms.CharField(
        label='Confirm Password',
        )
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')
    
    def clean_email(self):
        """
        Validate that email is unique
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already registered.')
        return email
    
    def clean_username(self):
        """
        Validate that username is unique
        """
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username
    
    def save(self, commit=True):
        """
        Save the user with first_name and last_name
        """
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
        return user               