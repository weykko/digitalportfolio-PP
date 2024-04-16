from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField

from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey


# Create your models here.


@register_snippet
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
    parent_page_types = ['home.HomePage']




