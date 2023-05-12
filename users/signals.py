#sendeer is the model that sends the exent
#created is true or false , true if created first time

from .models import Profile
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver # decorator for signals
from django.contrib.auth.models import User


@receiver(post_save,sender=User)
def profile_updated(sender,instance,created,**kwargs):
    if created:
        user = instance 
        profile = Profile.objects.create(user=user,username=user.username,email=user.email,name=user.first_name)
    print('profile saved')
    print('instance',instance)
    print('created',created)


@receiver(post_delete,sender=Profile)
def delete_user(sender,instance,**kwargs):
    user = instance.user 
    user.delete()
    print('deleting user')

@receiver(post_save,sender=Profile)
def updateUser(sender,instance,created,**kwargs):
    profile = instance 
    user = profile.user 
    if created==False:
        user.first_name = profile.name 
        user.username = profile.username 
        user.email = profile.email
        user.save()


# post_save.connect(profile_updated,sender=Profile)
# post_delete.connect(delete_user,sender=Profile)