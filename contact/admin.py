from django.contrib import admin
from contact.models import Contact, Category

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = 'id', 'first_name', 'last_name', 'phone',
    ordering = '-id',
    # list_filter = 'created_date',
    search_fields = 'first_name', 'id', 'last_name',
    list_per_page = 10
    list_max_show_all = 20
    list_editable = 'phone',

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'id', 'name',
    ordering = '-id',