import uuid

from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

from .validators import validate_icon_image_size,validate_image_file_exstension


def category_icon_upload_path(instance,filename):
    return f"category/{instance.name}/category_icon/{filename}"

def server_icon_upload_path(instance,filename):
    return f"server/{instance.name}/server_icon/{filename}"

def server_banner_upload_path(instance,filename):
    return f"server/{instance.name}/server_banner/{filename}"

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name  = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True,null=True)
    icon = models.FileField(
        upload_to=category_icon_upload_path,
                            null=True,
                            blank=True)
    def save(self,*args,**kwargs):
        if self.id:
            existing = get_object_or_404(Category,id=self.id)
            if existing.icon != self.icon:
                existing.icon.delete(save=False)
            super().save(*args,**kwargs)
    
    @receiver(models.signals.pre_delete, sender="server.Category")
    def category_delete_files(sender, instance,**kwargs):
        for field in instance._meta.fields:
            if field.name =='icon':
                file = getattr(instance,field.name)
                if file:
                    file.delete(save=False)
        
    
    def __str__(self):
        return self.name

class Server(models.Model):
    name  = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="server_owner")
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="server_category")
    description = models.CharField(max_length=250,blank=True,null=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name="server_members")
    def __str__(self):
        return self.name
    

class Channel(models.Model):
    name  = models.CharField(max_length=100, unique=True)
    owner= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="channel_owner")
    server = models.ForeignKey(Server,on_delete=models.CASCADE,related_name="channel_server")
    banner= models.ImageField(upload_to=server_banner_upload_path,null=True,blank=True,validators=[validate_image_file_exstension])
    icon= models.ImageField(upload_to=server_icon_upload_path,null=True,blank=True,validators=[validate_icon_image_size,validate_image_file_exstension])
   
    def save(self,*args,**kwargs):
        if self.id:
            existing = get_object_or_404(Channel,id=self.id)
            if existing.icon != self.icon:
                existing.icon.delete(save=False)
            if existing.banner != self.banner:
                existing.banner.delete(save=False)
            super().save(*args,**kwargs)
    
    @receiver(models.signals.pre_delete, sender="server.Category")
    def category_delete_files(sender, instance,**kwargs):
        for field in instance._meta.fields:
            if field.name =='icon' or field.name == 'banner':
                file = getattr(instance,field.name)
                if file:
                    file.delete(save=False)
        
    
    def __str__(self):
        return self.name
    