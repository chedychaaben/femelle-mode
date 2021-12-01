import datetime
import json
import string # for the id generator
import random # for the id generator
from django.contrib.auth import login as auth_login #pour la reconnection apres le changement de mot de passe
from django.contrib.auth import authenticate #pour la reconnection apres le changement de mot de passe
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404 , redirect
from django.template import RequestContext
from django.contrib import messages
from .models import SlideImg,Article,OrderArticle,Order,Adresse,OrderMessage,OrderState
from .forms import UserUpdateForm,ChangePasswordForm,AdresseCreateForm,AdresseUpdateForm
from .models import Account as User

User = get_user_model()

def handler404(request, *args, **argv):
    messages.warning(request, f'Erreur 404')
    return redirect('/')


def handler500(request, *args, **argv):
    messages.warning(request, f'Erreur 500')
    return redirect('/')

# Create your views here.
def homepage(request):
    context = {'SlideImgs' :SlideImg.objects.all(),
                'Articles' :Article.objects.all()}
    return render(request, 'homepage.html',context)

def cart(request):
    if request.user.is_authenticated:
        try:
            context = {
                    'selected_order': Order.objects.get(user=request.user, ordered=False)}
        except:
            context = {}
    else:
        context = {}
    return render(request, 'cart.html',context)
    
def articleView(request,slug):
    try:
        article = Article.objects.get(slug=slug)
    except:
        return redirect('/')
    context = {'article' : article
                }
    return render(request, 'product.html',context)


def updateItem(request): #for both guest and users
    data = json.loads(request.body) #{'articleId': '8', 'action': 'add'}
    articleId = data['articleId']   
    action = data['action']
    article = get_object_or_404(Article, id=articleId)
    device = request.COOKIES.get('device') 
    if request.user.is_authenticated:
        user = request.user


    if action == 'up':
        if request.user.is_authenticated:
            orderItem, created = OrderArticle.objects.get_or_create(article=article,user=user,ordered=False)
            order_qs = Order.objects.filter(user=user, ordered=False)
        else:
            orderItem, created = OrderArticle.objects.get_or_create(user=None,device=device,article=article,ordered=False)
            order_qs = Order.objects.filter(user=None,device=device, ordered=False)

        if order_qs.exists(): 
            order = order_qs [0]
            if order.orderarticles.filter(article__id=articleId).exists():
                orderItem.quantity += 1
                orderItem.save()
                messages.info(request, f'{article.title} quantity was updated !')
            else:
                order.orderarticles.add(orderItem)
                messages.info(request, f'Just added {article.title} to your cart !')
        else:
            if request.user.is_authenticated:
                order = Order.objects.create(user=user, device=device, ordered_date=timezone.now())
            else:
                order = Order.objects.create(user=None,device=device, ordered_date=timezone.now())
            order.orderarticles.add(orderItem)
        return JsonResponse('The fking item was added', safe=False)

    elif action == 'down':
        if request.user.is_authenticated:
            orderItem = OrderArticle.objects.get(article=article,user=user,ordered=False)
        else:
            orderItem = OrderArticle.objects.get(user=None,device=device, article=article,ordered=False)

        if orderItem.quantity > 1 :
            orderItem.quantity -= 1
            orderItem.save()
            messages.info(request, f'{article.title} quantity was updated !')
            return JsonResponse('Decreased', safe=False)
        else:
            pass
            return JsonResponse('Enzel Delete', safe=False)



    elif action == 'remove':
        try :
            if request.user.is_authenticated:
                OrderArticle.objects.get(article=article,user=user,ordered=False).delete()
            else:
                OrderArticle.objects.get(user=None,device=device, article=article,ordered=False).delete()
            messages.info(request, f'{article.title} Removed !')
            return JsonResponse('Removed', safe=False)
        except :
            return JsonResponse('This item isnt in ur cart', safe=False)
    else:
        return JsonResponse('Error', safe=False)


@login_required
def account(request):
    context = {
        'orders': Order.objects.filter(user=request.user, ordered=True),
        'adresse': Adresse.objects.filter(user=request.user).last(),
    }
    return render(request, 'account.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Votre compte a été bien modifié !')
            return redirect('/account') # you need to get him out because the user will get a weird message Of post request on hold 
            # if form are valid save than
    else:
        form = UserUpdateForm(instance=request.user)

    context = {
       'form': form
    }
    return render(request, 'profile.html' , context)
    

@login_required
def changepassword(request,id):
    selected_user = User.objects.get(id=id)
    if request.user == selected_user or request.user.is_superuser:
        password = selected_user.password
        form = ChangePasswordForm(request.POST or None)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            password2 = form.cleaned_data.get('password2')
            selected_user.set_password(password)
            selected_user.save()
            # sending message
            messages.success(request, f'Mot de passe modifié pour {selected_user}!')
            ## auto loggining in after sign up 
            auth_login(request, authenticate(email = request.user.email , password=password))
            return redirect('/account')
    context = {'selected_user':selected_user,
                'password':password,
                'form':form
                }
    return render(request, 'changepassword.html',context)


@login_required
def adresses(request):
    context = {
        'adresses': Adresse.objects.filter(user=request.user),
    }
    return render(request, 'adresses.html', context)


@login_required
def order_detail(request,id):
    context = {
        'order': Order.objects.filter(id=id,user=request.user, ordered=True)[0],
    }
    return render(request, 'order_detail.html', context)


@login_required
def addordermessage(request):
    try:
        if request.POST['orderarticle_id'] !="0":
            message = OrderMessage(user = request.user, text = request.POST['msgText'], orderarticle = OrderArticle.objects.get(id=request.POST['orderarticle_id']), related_to = Order.objects.get(id=request.POST['order_id']))
        else:
            message = OrderMessage(user = request.user, text = request.POST['msgText'], related_to = Order.objects.get(id=request.POST['order_id']))
        if request.method == 'POST' and request.POST['msgText'] != "":
            message.save()
            order = Order.objects.get(id=request.POST['order_id']).messages.add(message)
            messages.success(request, f'Message envoyé avec succès')
            return redirect(f"/orders/id_order={request.POST['order_id']}/#order-messages")
        else:
            messages.warning(request, f'Veuillez remplir tous les champs !')
            return redirect(f"/orders/id_order={request.POST['order_id']}/#order-messages")
    except:
        messages.warning(request, f'Erreur')
        return redirect('/')

@login_required
def deleteordermessage(request,id):
    message_this = OrderMessage.objects.get(id=id)
    if request.user == message_this.user or request.user.is_superuser :
        message_this.delete()
        messages.info(request, f'Message supprimer avec succès')
    else:
        messages.warning(request, f'Erreur')
    return redirect(f'/orders/id_order={message_this.related_to.id}/#order-messages')

@login_required
def cree_adresse(request):
    form = AdresseCreateForm(request.POST or None)
    if form.is_valid():
        form.instance.user = request.user
        form.instance.prenom = request.user.prenom
        form.instance.nom = request.user.nom
        telephone = form.cleaned_data.get('telephone')
        adresse = form.cleaned_data.get('adresse')
        adresse2 = form.cleaned_data.get('adresse2')
        codepostal = form.cleaned_data.get('codepostal')
        ville = form.cleaned_data.get('ville')
        form.save()
        messages.success(request, f'Adresse créé avec succès.')
        return redirect('/account/adresses')
    context = {
       'form': form
    }
    return render(request, 'adresse.html' , context)

@login_required
def modifieradresse(request,id):
    adresse_this = Adresse.objects.get(id=id)
    if request.user == adresse_this.user or request.user.is_superuser :
        if request.method == 'POST':
            form = AdresseUpdateForm(request.POST, instance=adresse_this)
            if form.is_valid():
                form.save()
                messages.success(request, f'Adresse a été mis à jour !')
                return redirect('/account/adresses')
        else:
            form = AdresseUpdateForm(instance=adresse_this)
        context = {
           'form': form,
           'adresse_this': adresse_this,
        }
        return render(request, 'adresse_edit.html' , context)
    messages.warning(request, f'Erreur')
    return redirect('/account/adresses')
    
    

@login_required
def deleteadresse(request,id):
    adresse_this = Adresse.objects.get(id=id)
    if request.user == adresse_this.user or request.user.is_superuser :
        adresse_this.delete()
    else:
        messages.warning(request, f'Erreur')
    return redirect('/account/adresses')

@login_required
def checkout(request,step):
    try:
        selected_order = Order.objects.get(user=request.user, ordered=False)
        # CHECKOUT INFORMATION LOGIQUE  
        if step == 'information':
            form = AdresseCreateForm(request.POST or None)
            if request.method == 'POST':
                selected_adresse = request.POST['selected_adresse']
                try:
                    if form.is_valid() and selected_adresse =="0":
                        form.instance.user = request.user
                        form.instance.prenom = request.user.prenom
                        form.instance.nom = request.user.nom
                        telephone = form.cleaned_data.get('telephone')
                        adresse = form.cleaned_data.get('adresse')
                        adresse2 = form.cleaned_data.get('adresse2')
                        codepostal = form.cleaned_data.get('codepostal')
                        ville = form.cleaned_data.get('ville')
                        form.save()
                        choosen_adresse = Adresse.objects.get(id=form.instance.id)
                    else:
                        choosen_adresse = Adresse.objects.get(id=selected_adresse)
                    #order .checkout_step step to  Livraison
                    selected_order.adresse = choosen_adresse
                    selected_order.checkout_step = 'livraison'
                    selected_order.save()
                    return redirect('/checkout/step=livraison/')
                except:
                    messages.warning(request, f'Erreur de selection Adresse ')

            context = {'adresses': Adresse.objects.filter(user=request.user),
                        'form':form,
                        'selected_order':selected_order,
                    }
            return render(request, 'checkout-information.html',context)
        # CHECKOUT LIVRAISON LOGIQUE    
        elif step == 'livraison':
            # if he skips immediatly to livraision without adding adress via URL
            try:
                adresse = selected_order.adresse
            except:
                messages.warning(request, f'Choisir une Adresse ')
                return redirect('/checkout/step=information/')
            if request.method == 'POST': 
                selected_order.checkout_step = 'paiement'
                selected_order.save()
                return redirect('/checkout/step=paiement/')
            context = {'adresse':adresse,
                    }
            return render(request, 'checkout-livraison.html',context)
        # CHECKOUT Paiement LOGIQUE    
        elif step =='paiement':
            try:
                adresse = selected_order.adresse
            except:
                messages.warning(request, f'Choisir une Adresse ')
                return redirect('/checkout/step=information/')
            if request.method == 'POST': 
                #order .checkout_step step to  finished
                selected_order.checkout_step = 'finished'
                selected_order.save()
                #make ordered True and create 
                #Action Taken to place the order
                # generate random order id
                def id_generator(size=6, chars=string.digits):
                    return ''.join(random.choice(chars) for _ in range(size))
                # generate random order id
                print(id_generator())
                try:
                    O = selected_order
                    OP = OrderArticle.objects.filter(user=request.user, ordered=False)

                    for element in range (len(OP)):
                        OP[element].ordered = True
                        OP[element].save()
                    O.prix = Order.get_total(O) # I CALLED THE FUNCTION OF THE MODEL HAHAH
                    O.ordered = True
                    O.transaction_id = id_generator()
                    O.save()
                    messages.success(request, f'Félicitations, Votre commande a bien été prise en compte.')
                except:
                    messages.warning(request, f'Confirmation Erreur !')
                    return redirect('/')
                #Action Taken to place the order
                return redirect(f'/orders/id_order={selected_order.id}/')
            context = {'adresse':adresse,}
            return render(request, 'checkout-paiement.html',context)
        #if someone trys to change the checkout step in link
        else:
            messages.warning(request, f'Erreur, Contactez nous !')
            return redirect('/panier')

    except:# CHECKOUT IF THERE IS NO ORDER CREATED BEFORE WHICH IS AN ERROR  
        messages.warning(request, f'Vous avez aucune Commande !')
        return redirect('/panier')
