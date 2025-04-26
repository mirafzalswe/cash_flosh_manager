from django.urls import path
from . import views

urlpatterns = [
    # Главная страница
    path('', views.IndexView.as_view(), name='index'),
    
    # Транзакции
    path('transactions/', views.TransactionListView.as_view(), name='transaction_list'),
    path('transactions/create/', views.TransactionCreateView.as_view(), name='transaction_create'),
    path('transactions/<int:pk>/edit/', views.TransactionUpdateView.as_view(), name='transaction_edit'),
    path('transactions/<int:pk>/delete/', views.TransactionDeleteView.as_view(), name='transaction_delete'),
    
    # API для динамической загрузки данных
    path('api/get-categories/', views.get_categories, name='get_categories'),
    path('api/get-subcategories/', views.get_subcategories, name='get_subcategories'),
    
    # Управление справочниками
    path('directories/', views.DirectoryListView.as_view(), name='directory_list'),
    
    # Управление статусами
    path('directories/status/create/', views.StatusCreateView.as_view(), name='status_create'),
    path('directories/status/<int:pk>/edit/', views.StatusUpdateView.as_view(), name='status_edit'),
    path('directories/status/<int:pk>/delete/', views.StatusDeleteView.as_view(), name='status_delete'),
    
    # Управление типами транзакций
    path('directories/transaction-type/create/', views.TransactionTypeCreateView.as_view(), name='transaction_type_create'),
    path('directories/transaction-type/<int:pk>/edit/', views.TransactionTypeUpdateView.as_view(), name='transaction_type_edit'),
    path('directories/transaction-type/<int:pk>/delete/', views.TransactionTypeDeleteView.as_view(), name='transaction_type_delete'),
    
    # Управление категориями
    path('directories/category/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('directories/category/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='category_edit'),
    path('directories/category/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
    
    # Управление подкатегориями
    path('directories/subcategory/create/', views.SubcategoryCreateView.as_view(), name='subcategory_create'),
    path('directories/subcategory/<int:pk>/edit/', views.SubcategoryUpdateView.as_view(), name='subcategory_edit'),
    path('directories/subcategory/<int:pk>/delete/', views.SubcategoryDeleteView.as_view(), name='subcategory_delete'),
]