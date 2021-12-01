from django import forms
from django.contrib.auth import authenticate, get_user_model
from .models import Profile
from .models import Account as User

User = get_user_model()

class UserLoginForm(forms.Form):
    email = forms.EmailField(label='Adresse e-mail ou numéro de tél :',widget=forms.TextInput(attrs={'placeholder': 'Adresse e-mail ou numéro de tél'}), help_text='Nous ne partagerons jamais votre e-mail avec qui que ce soit.')
    password = forms.CharField(label='Mot de Passe :', widget=forms.PasswordInput(attrs={'placeholder': 'Mot de Passe'})) # Pass hiding

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email , password=password)
            if not user and User.objects.filter(email=email).exists():
                raise forms.ValidationError("Le mot de passe entré est incorrect.")  #"Incorrect Password."
            
            if not user:
                raise forms.ValidationError("L’e-mail ou le numéro de téléphone entré ne correspond à aucun compte.")  #"Incorrect Username."

        return super(UserLoginForm,self).clean(*args,**kwargs)



class UserResigterForm(forms.ModelForm):
    prenom = forms.CharField(label='Prénom :',widget=forms.TextInput(attrs={'placeholder': 'Prénom'}),max_length=25)
    nom = forms.CharField(label='Nom :',widget=forms.TextInput(attrs={'placeholder': 'Nom'}),max_length=25)
    email = forms.EmailField(label='Adresse e-mail :',widget=forms.TextInput(attrs={'placeholder': 'Adresse e-mail'}),max_length=50, help_text='Nous ne partagerons jamais votre e-mail avec qui que ce soit.')
    password = forms.CharField(label='Mot de passe :*',widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'})) # Pass hiding
    password2 = forms.CharField(label='Confirmer Mot de passe :*',widget=forms.PasswordInput(attrs={'placeholder': 'Confirmer Mot de passe'})) # Pass hiding
    phone = forms.CharField(label='Numéro de téléphone :',widget=forms.NumberInput(attrs={'placeholder': 'Téléphone'}),max_length=30)
    class Meta:
        model = User
        fields = ['prenom', 'nom', 'email', 'password', 'password2', 'phone']
     
    def clean(self, *args, **kwargs):
        prenom = self.cleaned_data.get('prenom')
        nom = self.cleaned_data.get('nom')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        phone = self.cleaned_data.get('phone')
        if password != password2:
            raise forms.ValidationError('Le Mot de passe doit être identique !')
        
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("L'e-mail entré deja existe...")

        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError("Le numéro de téléphone entré deja existe...")

        def password_uncase_sensitiving(self):
            data = self.cleaned_data['password']
            data = self.cleaned_data['password2']
            return data.lower()

        return super(UserResigterForm, self).clean(*args,**kwargs)