from django import template
from django.urls import resolve
from menu.models import Menu, MenuItem

register = template.Library()

@register.simple_tag
def draw_menu(menu_name):
    menu = Menu.objects.get(name=menu_name)
    items = menu.items.filter(parent__isnull=True).prefetch_related('children')
    return items

@register.simple_tag
def draw_menu_item(item, active_url):
    subitems = item.children.all()
    active_class = 'active' if item.get_absolute_url() == active_url else ''
    
    html = f'<li class="{active_class}"><a href="{item.get_absolute_url()}">{item.title}</a>'
    
    if subitems:
        html += '<ul>'
        for subitem in subitems:
            html += draw_menu_item(subitem, active_url)
        html += '</ul>'
    
    html += '</li>'
    return html
