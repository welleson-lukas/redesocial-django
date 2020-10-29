from django.db import models
from django.contrib.auth.models import User
from .utils import get_random_code
from django.template.defaultfilters import slugify

class Perfil(models.Model):
    first_name = models.CharField(max_length=200, blank=True, verbose_name='Primeiro nome')
    last_name = models.CharField(max_length=200, blank=True, verbose_name='Ultimo nome')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default="sem bio...", max_length=400)
    email = models.EmailField(max_length=200, blank=True)
    pais = models.CharField(max_length=200, blank=True)
    avatar = models.ImageField(default='avatar.png', upload_to='avatars/')
    amigos = models.ManyToManyField(User, blank=True, related_name='amigos')
    slug = models.SlugField(unique=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}-{self.created.strftime('%d-%m-%Y')}"

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'


    def save(self, *args, **kwargs):
        ex = False
        if self.first_name and self.last_name:
            to_slug = slugify(str(self.first_name) + " " + str(self.last_name))
            ex = Perfil.objects.filter(slug=to_slug).exists()
            while ex:
                to_slug = slugify(to_slug + " " + str(get_random_code()))
                ex = Perfil.objects.filter(slug=to_slug).exists()
        else:
            to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args, **kwargs)



STATUS_CHOICE = (
    ('enviada', 'enviada'),
    ('aceita', 'aceita')
)

class Relationship(models.Model):
    sender = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=20, choices=STATUS_CHOICE,verbose_name='status da solicitação')

    def __str__(self):
        return f'{self.sender}-{self.receiver}-{self.status}'