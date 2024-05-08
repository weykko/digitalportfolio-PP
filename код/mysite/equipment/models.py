from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
class Profile(models.Model):
    profile_pic = models.ImageField(verbose_name="Аватарка", null=True, blank=True, upload_to="images/profile/")
    user = models.OneToOneField(User,verbose_name="Пользователь", on_delete=models.CASCADE)
    firstname = models.CharField(verbose_name="Имя", max_length=30)
    lastname = models.CharField(verbose_name="Фамилия", max_length=30)
    city = models.CharField(verbose_name="Город", max_length=30, null=True)
    bio=models.TextField(verbose_name="Расскажите о себе", null=True, blank=True)
    achievements = models.TextField(verbose_name="Достижения", null=True, blank=True)
    VK = models.CharField(verbose_name="Ваш Вконтакте", max_length=50, null=True, blank=True)
    Telegram = models.CharField(verbose_name="Ваш Телеграм", max_length=50, null=True, blank=True)
    WhatsApp = models.CharField(verbose_name="Ваш WhatsApp", max_length=50, null=True, blank=True)
    #mail = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.pk = self.user.pk

        super(Profile, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('user_profile', kwargs={'pk': self.pk})

'''@register_snippet
class PortfolioOperator(models.Model):
    """Оператор портфолио"""

    name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField()

    portfolio = ParentalKey(
        'equipment.PorfolioPage',
        related_name='operators'
        )

class PortfolioPage(Page):
    """Портфолио. Мои работы"""

    description = RichTextField(
        blank=True,
        null=True,
        features=['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 
                  'hr', 'bold', 'italic', 'ol', 'ul', 'link']
    )

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        InlinePanel('operators')
    ]

    subpage_types = []
    parent_page_types = ['equipment.EquipmentIndexPage']

    class Meta:
        verbose_name = 'Мои работы'
        verbose_name_plural = 'Мои работы'

class PortfolioIndexPage(Page):
    """Страница для выведения ленты с работами"""

    subpage_types = ['equipment.PortfolioPage']
    parent_page_types = ['home.HomePage']'''