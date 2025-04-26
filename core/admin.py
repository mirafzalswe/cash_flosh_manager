from django.contrib import admin
from .models import Status, TransactionType, Category, Subcategory, Transaction


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(TransactionType)
class TransactionTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'transaction_type')
    list_filter = ('transaction_type',)
    search_fields = ('name',)
    ordering = ('name',)
    autocomplete_fields = ['transaction_type']


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)
    ordering = ('name',)
    autocomplete_fields = ['category']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'status', 'transaction_type', 'category', 'subcategory', 'amount', 'created_at')
    list_filter = ('status', 'transaction_type', 'category', 'subcategory', 'date')
    search_fields = ('comment',)
    ordering = ('-date', '-created_at')
    date_hierarchy = 'date'
    autocomplete_fields = ['status', 'transaction_type', 'category', 'subcategory']
    readonly_fields = ('created_at', 'updated_at')
