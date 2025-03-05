from django.contrib import admin
from  .models import Channel,Server,Category

import uuid

class CategoryAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # Ensure the ID is properly converted to UUID before saving
        if isinstance(obj.id, str):  # If the ID is a string
            obj.id = uuid.UUID(obj.id)
        super().save_model(request, obj, form, change)

admin.site.register(Category, CategoryAdmin)


admin.site.register(Channel)
admin.site.register(Server)
