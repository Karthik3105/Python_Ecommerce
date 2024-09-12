from django.contrib import admin

# Register your models here.
from .models import Category, Product

class CategoryAdmin(admin.ModelAdmin):
    # Specify the fields to display in the admin list view
    list_display = ('category_id', 'category_code', 'category_description', 'created_on')
    # list_editable = ('category_code', 'category_description')
    # Optional: Add search and filter capabilities
    search_fields = ('category_code', 'category_description')
    list_filter = ('created_on',)

admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    # Specify the fields to display in the admin list view
    list_display = (
        'product_id', 'category', 'category_id', 'product_name', 
        'product_details', 'product_image', 'created_by', 'created_on'
    )
    # Optional: Add search and filter capabilities
    list_editable = ('category','product_name', 'product_details','product_image')
    search_fields = ('product_name', 'category__category_code')
    list_filter = ('created_on', 'category')

    # No need to set category_code in save_model anymore
    def save_model(self, request, obj, form, change):
        # No manual setting of category_code here if it's a property
        super().save_model(request, obj, form, change)

admin.site.register(Product, ProductAdmin)
