#       -*- coding: utf-8 -*-
from django.template import Library

__author__ = 'papousek'

register = Library()

@register.filter
def get_range(value):
  return range(value)