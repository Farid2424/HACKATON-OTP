from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from . import forms
from django.views.generic import View
from django.conf import settings 
from .forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import TacheForm
from .models import Tache
from django.core.mail import send_mail
from django_otp.plugins.otp_email.models import EmailDevice
# views.py
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirection vers la page OTP
                return redirect('two_factor:login')  # La page de saisie du code OTP
            else:
                form.add_error(None, 'Identifiants incorrects')
    else:
        form = AuthenticationForm()

    return render(request, 'my_app/login.html', {'form': form})

def validate_otp_code(user, otp_code):
    device = EmailDevice.objects.get(user=user)
    if device.verify_token(otp_code):
        return True
    return False

def send_otp_email(user):
    # Créer un objet EmailDevice pour l'utilisateur
    device = EmailDevice.objects.create(user=user)
    
    # Générer un OTP
    otp_code = device.generate_challenge()

    # Envoyer l'OTP par email
    send_mail(
        'Votre code OTP',
        f'Votre code OTP est : {otp_code}',
        'no-reply@votre_domaine.com',
        [user.email],
    )
    return otp_code
class PasswordChangeView(View):
    def post(self,request):
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
             # Met à jour la session avec le nouveau mot de passe
            messages.success(request, 'Votre mot de passe a été modifié avec succès.')
            return redirect('profile')  # Redirigez vers la page du profil ou une autre page appropriée
    def get(self,request):
        form = PasswordChangeForm()
        return render(request, 'pass_change.html', {'form': form})
    

class PasswordChangeDoneView(View):
    template_name='host/password_change_done.html'
    def get(self, request):
        message = ''
        return render(request, self.template_name, context={'message': message})
    def post(self, request):
        form = self.form_class(request.POST)   

class LoginPage(View):
    template_name = 'authentication/login.html'
    form_class = forms.LoginForm

    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={'form': form,'message': message})
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('home')
        message = 'Identifiants invalides.'
        return render(request, self.template_name, context={'form': form, 'message': message})
    


class Logout_user(View):
    def post(self,request):
        logout(request)
        return redirect('home')

def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(settings.LOGIN_URL)
    return render(request, 'authentication/signup.html', context={'form': form})
 # Create your views here.
def home(request):
   if not request.user.is_authenticated:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")
   context = {'message': 'Bienvenue sur la page d\'accueil !'}
   return render(request, 'home.html', context)
def tache(request):
    form = forms.TacheForm()
    if request.method == 'POST':
        form = forms.TacheForm(request.POST)
        if form.is_valid():
            tache_s=form.save()
            tache_id=tache_s.id
            return redirect('after_tache', tache_id=tache_id)     
    return render(request,'tache.html', context={'form': form})

def after_tache(request,tache_id):
    tache = get_object_or_404(Tache, pk=tache_id)
    context = {'tache': tache}
    return render(request, 'after_tache.html', {'tache': tache})


from django.shortcuts import redirect
from django_otp.forms import OTPAuthenticationForm
from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == "POST":
        # Récupérer les identifiants de l'utilisateur
        username = request.POST['username']
        password = request.POST['password']
        
        # Authentifier l'utilisateur
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Connexion de l'utilisateur
            login(request, user)
            
            # Vérifier si l'utilisateur a un dispositif OTP actif
            if user.has_otp_device():
                # Rediriger vers la page de validation OTP
                return redirect('two_factor:login')  # Ou la vue où l'utilisateur entre son OTP
                
            return redirect('home')  # Rediriger vers la page d'accueil ou une autre page
        else:
            # Utilisateur non valide
            return redirect('login')
    
    return render(request, 'login.html')
            
"""class Taches(View):
    model = Tache
    template_name = 'after_tache.html'
    form_class = TacheForm
    def get(self, request):
        message = ''
        return render(request, self.template_name, context={'message': message})
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return render(request, self.template_name,
                          {'message': 'Tâche créée avec succès'})
        return render(request, self.template_name, {'form': form})"""