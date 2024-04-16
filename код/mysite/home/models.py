from django.db import models

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField, StreamField

from wagtail.blocks import RichTextBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock

from .blocks import FigCaptionBlock

from wagtail.snippets.models import register_snippet

@register_snippet
class Footer(models.Model):

    bodytext = RichTextField()

    panels = [
        FieldPanel('bodytext')]
    

    class Meta:
        verbose_name = "Футер"
        verbose_name_plural = "Футеры"
    def __str__(self):
        return "Футер"



class AutorizationPage(Page):

    template = 'home/autorization_page.html'

    pass


class HomePage(Page):

    subpage_types = ['home.AutorizationPage']

    parent_page_types = []


    # поля в базе данных
    subtitle = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name = "Подзаголовок"
    )

    rtfbody = RichTextField(
        blank=True,
        null=True
    )

    body = StreamField(
        [('figcaptionblock', FigCaptionBlock()),
        ('rtfblock', RichTextBlock(
            #features = ['h1', 'h6', 'hr', 'bold', 'italic', 'link'],
            label = 'Текст', 
            help_text = 'Введите описание',)),
         ('imgblock', ImageChooserBlock(
             label = 'Вставить картиночку',
             template = 'blocks/imgblock.html' 
                                        )),
         ('streamfieldblock', EmbedBlock(label = 'эээ вроде видос какой то вставить можно'))     
    ], 
    blank = True

    )

    publish_image = models.ForeignKey(
        'wagtailimages.Image', 
        blank=True,
        null=True,
        on_delete = models.SET_NULL,
        related_name = '+'
    )
 

    # поля для ввода данных в интерфейсе администратора
    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('body'),
        #FieldPanel('rtfbody'),
        FieldPanel('publish_image')
    ]

    #promote_panels = []
    #settings_panels = []
