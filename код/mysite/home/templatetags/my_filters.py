from django.template.loader_tags import register


@register.inclusion_tag("blocks/comment.html")
def place_comment(comment):
    return {'comment': comment}