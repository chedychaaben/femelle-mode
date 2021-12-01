from django.contrib import admin
from django.urls import path, include, re_path
#static files and media files importation
from django.conf import settings
from django.conf.urls.static import static
#static files and media files importation
import femalemodeapp.views as femalemodeappviews
import users.views as usersviews


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',femalemodeappviews.homepage, name='homepage'),
    path('panier/',femalemodeappviews.cart, name='cart'),
    path('account/',femalemodeappviews.account, name='account'),
    path('account/adresses/',femalemodeappviews.adresses, name='adresses'),
    path('orders/id_order=<id>/',femalemodeappviews.order_detail, name='order_detail'),
    path('collection/<slug>/',femalemodeappviews.articleView, name='articleView'),
    path('update_item/', femalemodeappviews.updateItem,name='update_item'),
    path('addordermessage/', femalemodeappviews.addordermessage,name='addordermessage'),
    path('deleteordermessage/<id>/', femalemodeappviews.deleteordermessage,name='deleteordermessage'),
    path('adresse/', femalemodeappviews.cree_adresse,name='cree_adresse'),
    path('modifieradresse/<id>/', femalemodeappviews.modifieradresse,name='modifieradresse'),
    path('deleteadresse/<id>/', femalemodeappviews.deleteadresse,name='deleteadresse'),
    path('checkout/step=<step>/', femalemodeappviews.checkout,name='checkout'),
    
    path('account/profile/',femalemodeappviews.profile, name='profile'),
    path('account/profile/<id>/changer-mot-de-passe/',femalemodeappviews.changepassword, name='changepassword'),
    # AUTHENTIFICATION URLS
    path('connexion/',usersviews.login, name='login'),
    path('account/logout',usersviews.logout, name='logout'),
    path('inscription/',usersviews.signup, name='signup'),
    # AUTHENTIFICATION URLS
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'femalemodeapp.views.handler404'
handler500 = 'femalemodeapp.views.handler500'