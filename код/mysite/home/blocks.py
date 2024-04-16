from wagtail.blocks import StructBlock, CharBlock
from wagtail.images.blocks import ImageChooserBlock


class FigCaptionBlock(StructBlock):

    figure = ImageChooserBlock(label = 'Вставьте КаРтИнКу')
    caption = CharBlock(label = 'Добавьте описание по браски жи ес')


    class Meta:
        icon = 'image'
        template = 'blocks/fig_caption_block.html'
        label = 'Картинка с подписью'