from django.contrib.admin.templatetags.admin_list import pagination
from django.template import Library

register = Library()

@register.inclusion_tag('utils/pagination.html')
def result_pagination(cl):
	return pagination(cl)