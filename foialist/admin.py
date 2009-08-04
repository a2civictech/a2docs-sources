from django.contrib import admin
from foialist.models import *


class EntryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

class EntityAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class ReasonAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(File)
admin.site.register(Comment)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Entity, EntityAdmin)
admin.site.register(Reason, ReasonAdmin)