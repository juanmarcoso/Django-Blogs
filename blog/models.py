from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
# Aqui vamos a crear nuestras tablas

# Vamos a crear nuestro propio manager
class PublishManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
            .filter(status=Post.Status.PUBLISHED)
    
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish') # Va a hacer que sea unico por fecha
    author = models.ForeignKey(User, 
                               on_delete=models.CASCADE, # Si yo elimino un usuario, borra todo en cascada
                               related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now) #Vamos a poder ponerle nosotros la fecha
    created = models.DateTimeField(auto_now_add=True) #Se actualiza solo cuando se crea
    updated = models.DateTimeField(auto_now=True) #Se actualiza cada vez que se actualiza
    status = models.CharField(max_length=2, # Solo dos opciones (borrado o publicado)
                              choices=Status.choices,
                              default=Status.DRAFT) # Por defecto definimos que va a estar en un estado de borrador
    # Armando nuestros manahers dentro de la clase
    objects = models.Manager()
    published = PublishManager()
    
    class Meta:
        # Con esta clase, queremos que los datos se ordenen de forma inversa desde la variable publish
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]
    
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse ('blog:post_detail', args=[self.publish.year,
                                                  self.publish.month,
                                                  self.publish.day,
                                                  self.slug])
    