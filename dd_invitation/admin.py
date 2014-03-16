# -*- coding: utf-8 -*-

from dd_invitation import models

from django.contrib import admin

class TokenAdmin(admin.ModelAdmin):
  list_display = ('value', 'consumed', 'created')
  ordering  = ('-created',)

  class Media:
    js = ('dd_invitation.js',)

admin.site.register(models.Token, TokenAdmin)
