from django.contrib import admin
from .models import SlideImg,Article,ArticleImage,OrderArticle,Order,Adresse,OrderMessage,OrderState
# Register your models here.
admin.site.register(SlideImg)
admin.site.register(Article)
admin.site.register(ArticleImage)
admin.site.register(Adresse)
admin.site.register(OrderArticle)
admin.site.register(Order)
admin.site.register(OrderMessage)
admin.site.register(OrderState)
