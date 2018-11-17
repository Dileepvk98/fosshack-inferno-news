# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Articles,Categories,Category_Source,MarkedNews,SourcesSelected

# Register your models here.
admin.site.register(Articles)
admin.site.register(Categories)
admin.site.register(Category_Source)
admin.site.register(MarkedNews)
admin.site.register(SourcesSelected)