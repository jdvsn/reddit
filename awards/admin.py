from django.contrib import admin

from .models import Award

class AwardAdmin(admin.ModelAdmin):
    fields = ['tier', 'purchased_by', 'sent_to']
admin.site.register(Award, AwardAdmin)

