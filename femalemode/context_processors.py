from femalemodeapp.models import OrderArticle
from django.contrib.auth import authenticate

# This works because i added in setting.py in Templates list 'femalemode.context_processors.context_to_all_templates'

def context_to_all_templates(request):
    quantity_of_articles = 0
    cart_total = 0
    if request.user.is_authenticated:
        biglist = OrderArticle.objects.filter(user=request.user, ordered=False)
        for element in range (len(biglist)):
            quantity_of_articles += biglist[element].quantity
            cart_total += (biglist[element].article.prix * biglist[element].quantity)
        count_articles = len(biglist)
        all_orderarticles = OrderArticle.objects.filter(user=request.user, ordered=False)

    else:
        device = request.COOKIES.get('device') 
        biglist = OrderArticle.objects.filter(user=None,device=device, ordered=False)
        for element in range (len(biglist)):
            quantity_of_articles += biglist[element].quantity
            cart_total += (biglist[element].article.prix * biglist[element].quantity)
        count_articles = len(biglist)
        all_orderarticles = OrderArticle.objects.filter(user=None,device=device,ordered=False)

    return {'quantity_of_articles': quantity_of_articles, 
            'cart_total': cart_total , 
            'count_articles': count_articles ,
            'all_orderarticles':all_orderarticles ,
            }