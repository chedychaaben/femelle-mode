import datetime
from django_extensions.db.fields import AutoSlugField
from django.template.defaultfilters import slugify
from django.db import models
from PIL import Image
from users.models import Account

OrderStateText_CHOICES = (
    ('0','Anuler'),
    ('1','En cours de préparation'),
    ('2','Commande confirmée'),
    ('3','Expédié'),
)
OrderStateColor_CHOICES = (
    ('0','#FF0000'),
    ('1','#FFA500'),
    ('2','#00FF7F'),
    ('3','#006400'),
)

# Create your models here.
class SlideImg(models.Model):
    image = models.ImageField(upload_to='sliderImgs')
    def  __str__(self):
        return str(self.image)

    #Save The image at 1520*600 px
    def save(self, ** kwargs): # the save method is already exist we r just modifing it
        super().save() # save the the user gave in large size

        img = Image.open(self.image.path)
        
        output_size = (1520, 800)
        img.thumbnail(output_size)
        img.save(self.image.path)
    #Save The image at 1520*600 px


        
class ArticleImage(models.Model):
    image = models.ImageField(upload_to='ArticleImgs')
    def  __str__(self):
        return str(f'{self.image}')
        
    #Save The image at 800*3600 px
    def save(self, ** kwargs):
        super().save()

        img = Image.open(self.image.path)

        output_size = (800, 3600)
        img.thumbnail(output_size)
        img.save(self.image.path)
    #Save The image at 800*3600 px

class Article(models.Model):
    title = models.CharField(max_length=60)
    prix = models.DecimalField(default=0, max_digits=8, decimal_places=3)
    discount_prix = models.DecimalField(default=0, max_digits=7, decimal_places=3, null=True,blank=True)
    description = models.TextField(default='', null=True)
    label = models.TextField(default='', null=True)
    size = models.TextField(default='', null=True)
    color = models.TextField(default='', null=True)
    published = models.DateTimeField(default=datetime.datetime.now())
    images = models.ManyToManyField(ArticleImage, related_name='images')
    slug = AutoSlugField(('slug'), max_length=30, unique=True, populate_from=('title'))
    
    def  __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super(Article, self).save(*args, **kwargs)



class OrderArticle(models.Model): # create and order from that product taken
    user = models.ForeignKey(Account,
                            on_delete=models.CASCADE, blank=True, null=True)
    
    device = models.CharField(max_length=40, blank=True, null=True)

    article = models.ForeignKey(Article, on_delete=models.SET_NULL, blank=True, null=True)  #REMOVE NULLS
    quantity = models.IntegerField(default=1) # setting the quantity 
    ordered = models.BooleanField(default=False)
    
    def  __str__(self):
        if self.user == None :
            return f"{self.quantity} X {self.article} - GuestUser {self.device} " 
        return f"{self.quantity} X {self.article} - {self.user.email}" 
        

    def get_total_article_prix(self):
        return self.quantity * self.article.prix


class Adresse(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE, blank=True, null=True)
    prenom = models.CharField(max_length=50)
    nom = models.CharField(max_length=50)
    societe = models.CharField(max_length=50, blank=True, null=True)
    adresse = models.CharField(max_length=50)
    adresse2 = models.CharField(max_length=50, blank=True, null=True)
    codepostal = models.CharField(max_length=50, blank=True, null=True)
    ville = models.CharField(max_length=50)
    telephone = models.CharField(max_length=50)
    
    def  __str__(self):
        if self.user == None :
            return f"{self.adresse} X {self.ville}" 
        return f"{self.adresse} X {self.ville} - {self.user.email}" 
        
class OrderMessage(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE, blank=True, null=True)
    text = models.TextField(max_length=250, blank=True, null=True)
    related_to = models.ForeignKey('femalemodeapp.Order',on_delete=models.CASCADE, blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    orderarticle =  models.ForeignKey('femalemodeapp.Orderarticle', on_delete=models.CASCADE , blank=True, null=True)
    
    def  __str__(self):
        if self.user == None :
            return f"Message Related To Order : {self.related_to.id}" 
        return f"Message of {self.user} Related To Order : {self.related_to.id}" 

class OrderState(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE, blank=True, null=True)
    text = models.CharField(choices=OrderStateText_CHOICES,max_length=50)
    color = models.CharField(choices=OrderStateColor_CHOICES,max_length=50,blank=True, null=True,editable=False)
    related_to = models.ForeignKey('femalemodeapp.Order',on_delete=models.CASCADE, blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    
    def  __str__(self):
        if self.user == None :
            return f"{self.related_to} - {self.state}" 
        return f"{self.user} - Order : {self.related_to.id} - Statut : {self.text}" 

    def save(self, *args, **kwargs):
        self.color = self.text
        return super(OrderState, self).save(*args, **kwargs)
    


class Order(models.Model): 
    # assign the product to the order
    #if the user has and order already otherwise 
    #create a new order and assign the item in it
    user = models.ForeignKey(Account,
                            on_delete=models.CASCADE, blank=True, null=True)
    
    orderarticles = models.ManyToManyField(OrderArticle) # this just to check if item is mawjoud to add quantity

    creation_date = models.DateTimeField(auto_now_add=True)

    device = models.CharField(max_length=40, blank=True, null=True)

    transaction_id = models.CharField(max_length=10, blank=True, null=True,unique=True)

    ordered_date = models.DateTimeField() # LATER !! WE WILL BE CREATED THE moment the user finish his order

    ordered = models.BooleanField(default=False)# Status of the order DONE OR NOT YET

    prix =  models.DecimalField(default=0, max_digits=20, decimal_places=3)

    adresse = models.ForeignKey(Adresse,on_delete=models.CASCADE, blank=True, null=True)

    messages = models.ManyToManyField(OrderMessage, blank=True)

    states = models.ManyToManyField(OrderState, blank=True)

    checkout_step = models.CharField(max_length=40, blank=True, null=True)
    def  __str__(self):
        if self.user == None :
            return f"GuestUser {self.id}  - Started at : {self.creation_date.strftime('%H:%M:%S %A, %d %B %Y')} "
        return f"{self.user.email} - Started at : {self.creation_date.strftime('%H:%M:%S %A, %d %B %Y')} "

    def get_total(self):
        total = 0
        for order_item in self.orderarticles.all():
            total += order_item.get_total_article_prix()
        return total