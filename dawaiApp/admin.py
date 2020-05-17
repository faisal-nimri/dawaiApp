from django.contrib import admin
from .models import blog, product, category, user, drug, drugStore, review,question


# class blogAdmin(admin.ModelAdmin):
#     pass


admin.site.register(blog)
admin.site.register(category)
admin.site.register(product)
admin.site.register(user)
admin.site.register(drug)
admin.site.register(drugStore)
admin.site.register(review)
admin.site.register(question)
# Register your models here.



