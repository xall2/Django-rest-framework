from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User,related_name='profile',on_delete=models.CASCADE)  #كل يوزر عنده بروفايل واحد
    reset_password_token = models.CharField(max_length=50, default="",blank=True)
    reset_password_expire = models.DateTimeField(null=True, blank=True)




#تلقائي يسوي بروفايل لكل مستخدم جديد
@receiver(post_save, sender=User)
def save_profile(sender,instance,created, **kwargs): #الانستانس هوا اليوزر اللي تم انشاءه

    print('instance',instance)
    user = instance
    
    if created:   #اذا تم صناعة اليوزر
        profile = Profile(user=user) #يمرره هنا
        profile.save()

     
    
     