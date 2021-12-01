from django import forms
from django.contrib.auth import authenticate, get_user_model
from .models import Adresse
from .models import Account as User

User = get_user_model()

class UserUpdateForm(forms.ModelForm):
    prenom = forms.CharField(label='Prénom :',widget=forms.TextInput(attrs={'placeholder': 'Prénom'}),max_length=25)
    nom = forms.CharField(label='Nom :',widget=forms.TextInput(attrs={'placeholder': 'Nom'}),max_length=25)
    email = forms.EmailField(label='Adresse e-mail :',widget=forms.TextInput(attrs={'placeholder': 'Adresse e-mail'}),max_length=50, help_text='Nous ne partagerons jamais votre e-mail avec qui que ce soit.')
    phone = forms.CharField(label='Numéro de téléphone :',widget=forms.NumberInput(attrs={'placeholder': 'Téléphone'}),max_length=30)
    class Meta:
        model = User
        fields = ['prenom', 'nom', 'email', 'phone']

class ChangePasswordForm(forms.ModelForm):
    password = forms.CharField(label='Nouveau Mot de passe:',widget=forms.PasswordInput(attrs={'placeholder': 'Nouveau Mot de passe'})) # Pass hiding
    password2 = forms.CharField(label='Confirmer Mot de passe:',widget=forms.PasswordInput(attrs={'placeholder': 'Confirmer Mot de passe'})) # Pass hiding

    class Meta:
        model = User
        fields = ['password', 'password2']
     
    def clean(self, *args, **kwargs):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError('Mot de passe doit être identique !')
        return super(ChangePasswordForm, self).clean(*args,**kwargs)

class AdresseCreateForm(forms.ModelForm):
    #prenom = forms.CharField(label='Prénom :',widget=forms.TextInput(attrs={'placeholder': 'Prénom'}),required=False)
    #nom = forms.CharField(label='Nom :',widget=forms.TextInput(attrs={'placeholder': 'Nom'}),required=False)
    telephone = forms.DecimalField(label='Téléphone :',widget=forms.TextInput(attrs={'placeholder': 'Téléphone'}))
    #societe = forms.CharField(label='Société :',widget=forms.TextInput(attrs={'placeholder': 'Société'}),required=False)
    adresse = forms.CharField(label='Adresse :',widget=forms.TextInput(attrs={'placeholder': 'Adresse'}))
    adresse2 = forms.CharField(label="Complément d'adresse :",widget=forms.TextInput(attrs={'placeholder': "Complément d'adresse (optionnel)"}),required=False)
    codepostal = forms.CharField(label='Code postal :',widget=forms.TextInput(attrs={'placeholder': 'Code postal (optionnel)'}),required=False)
    ville = forms.CharField(label='Ville :',widget=forms.TextInput(attrs={'placeholder': 'Ville (optionnel)'}),required=False)

    class Meta:
        model = Adresse
        fields = ['telephone', 'adresse', 'adresse2', 'ville', 'codepostal']#'prenom', 'nom', 'societe', 

class AdresseUpdateForm(forms.ModelForm):
    prenom = forms.CharField(label='Prénom :',widget=forms.TextInput(attrs={'placeholder': 'Prénom (optionnel)'}),required=False)
    nom = forms.CharField(label='Nom :',widget=forms.TextInput(attrs={'placeholder': 'Nom (optionnel)'}),required=False)
    telephone = forms.DecimalField(label='Téléphone :',widget=forms.TextInput(attrs={'placeholder': 'Téléphone'}))
    societe = forms.CharField(label='Société :',widget=forms.TextInput(attrs={'placeholder': 'Société (optionnel)'}),required=False)
    adresse = forms.CharField(label='Adresse :',widget=forms.TextInput(attrs={'placeholder': 'Adresse'}))
    adresse2 = forms.CharField(label="Complément d'adresse :",widget=forms.TextInput(attrs={'placeholder': "Complément d'adresse (optionnel)"}),required=False)
    codepostal = forms.CharField(label='Code postal :',widget=forms.TextInput(attrs={'placeholder': 'Code postal (optionnel)'}),required=False)
    ville = forms.CharField(label='Ville :',widget=forms.TextInput(attrs={'placeholder': 'Ville (optionnel)'}),required=False)

    class Meta:
        model = Adresse
        fields = ['prenom', 'nom', 'societe', 'telephone', 'adresse', 'adresse2', 'ville', 'codepostal']