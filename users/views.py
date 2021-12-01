import datetime
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .forms import  UserLoginForm,UserResigterForm
from femalemodeapp.models import Article,OrderArticle,Order


# Create your views here.
def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    next = request.GET.get('next')
    form = UserResigterForm(request.POST or None)
    if form.is_valid():
        prenom = form.cleaned_data.get('prenom')
        nom = form.cleaned_data.get('nom')
        email = form.cleaned_data.get('email')
        phone = form.cleaned_data.get('phone')
        theuserfromsignup = form.save(commit=False)
        password = form.cleaned_data.get('password')
        theuserfromsignup.set_password(password)
        theuserfromsignup.save()
        
        # auto loggining in after sign up 
        new_user = authenticate(email = theuserfromsignup.email , password=password)
        auth_login(request, new_user)
        # sending message
        messages.success(request, f'{nom} {prenom} compte a bien été créé, Vous êtes automatiquement connecté !')
        #
        if next:
            return redirect(next)
        return redirect('/')
    context = {
       'form': form
    }
    return render(request, 'signup.html' , context)





def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(email = email , password=password)
        auth_login(request, user)
        getcartdata(request)
        messages.success(request, f'Vous êtes maintenant connecté !')
        if next:
            return redirect(next)
        return redirect('/panier')
    context = {
        'form': form
    }
    return render(request, 'login.html' , context)

def getcartdata(request):
    device = request.COOKIES.get('device') 

    GuestOrderArticles = OrderArticle.objects.filter(user=None,device=device, ordered=False)
    for i in range(len(GuestOrderArticles)):
        this_orderarticle = GuestOrderArticles[i]
        orderarticle_in_usertable_qs = OrderArticle.objects.filter(user=request.user, ordered=False,article=this_orderarticle.article)
        if orderarticle_in_usertable_qs.exists():
            orderarticle_in_usertable = orderarticle_in_usertable_qs[0]
            orderarticle_in_usertable.quantity += this_orderarticle.quantity
            orderarticle_in_usertable.save()
            this_orderarticle.delete()
        else:
            orderItem = OrderArticle.objects.create(user=request.user, ordered=False,quantity=this_orderarticle.quantity,article=this_orderarticle.article)
            authuser_order = Order.objects.filter(user=request.user,ordered=False) 
            if not authuser_order.exists(): #if the user dont have an order in its accoung then create it and add the item
                Order.objects.create(user=request.user,ordered=False, ordered_date=timezone.now()).orderarticles.add(orderItem)
            else: #if the user dont have an order in its accoung then create it and add the item
                authuser_order[0].orderarticles.add(orderItem)
            this_orderarticle.delete()
    try: #i just try because the guest user might login without adding anything to cart
        Order.objects.get(user=None,device=device,ordered=False).delete()
    except:
        pass


@login_required
def logout(request):
    auth_logout(request)
    messages.info(request, f'Vous êtes maintenant Deconnecté !')
    return redirect('/')

#messages.debug
#messages.info
#messages.success
#messages.success(request, f'Account Created, You can now log in {username}!')
#messages.warning
#messages.error