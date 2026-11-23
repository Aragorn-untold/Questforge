from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    for k, val in kwargs.items():
        if val is not None:
            updated[k] = val
        else:
            updated.pop(k, None)
    return updated.urlencode()
