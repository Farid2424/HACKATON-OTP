from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import User, Tache

class TacheForm(forms.ModelForm):
  class Meta:
    model = Tache
    fields = ['titre', 'description']
    
class PasswordChangeForm(forms.ModelForm):
    old_password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe actuel")
    new_password1 = forms.CharField(widget=forms.PasswordInput, label="Nouveau mot de passe")
    new_password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmez le nouveau mot de passe")

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get("old_password")
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")


        user = self.instance
        if not user.check_password(old_password):
            raise forms.ValidationError("Le mot de passe actuel est incorrect.")
        if new_password1 != new_password2:
            raise forms.ValidationError("Les nouveaux mots de passe ne correspondent pas.")
        return cleaned_data

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name' )

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label='Nom d’utilisateur')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label='Mot de passe')

