from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile
from .models import Account as User


#Each time a user is created the profile Create automatic 
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance) # the profile is created with user = Instance of the user him self
    #Save the profile 
        instance.profile.save()

#Each time a user log in 
#@receiver(post_save, sender=User)
#def getcartdata(sender, instance, **kwargs):