from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Sum, Q, F
from django.utils import timezone
from datetime import timedelta

from .models import Transaction, Status, TransactionType, Category, Subcategory
from .forms import (
    TransactionForm, TransactionFilterForm, StatusForm, 
    TransactionTypeForm, CategoryForm, SubcategoryForm
)


class IndexView(TemplateView):
    """Представление для главной страницы"""
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Получаем статистику за последние 30 дней
        today = timezone.now().date()
        thirty_days_ago = today - timedelta(days=30)
        
        # Общая сумма пополнений за последние 30 дней
        income_sum = Transaction.objects.filter(
            date__gte=thirty_days_ago,
            transaction_type__name='Пополнение'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Общая сумма списаний за последние 30 дней
        expense_sum = Transaction.objects.filter(
            date__gte=thirty_days_ago,
            transaction_type__name='Списание'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Общий баланс за все время
        total_income = Transaction.objects.filter(
            transaction_type__name='Пополнение'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        total_expense = Transaction.objects.filter(
            transaction_type__name='Списание'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        total_balance = total_income - total_expense
        
        context.update({
            'recent_transactions': Transaction.objects.all().order_by('-date')[:10],
            'income_sum': income_sum,
            'expense_sum': expense_sum,
            'total_balance': total_balance,
            'month_balance': income_sum - expense_sum
        })
        
        return context


class TransactionListView(ListView):
    """Представление для списка транзакций с фильтрацией"""
    model = Transaction
    template_name = 'transaction/list.html'
    context_object_name = 'transactions'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Transaction.objects.all().select_related(
            'status', 'transaction_type', 'category', 'subcategory'
        )
        
        # Применяем фильтрацию, если форма фильтрации отправлена
        filter_form = TransactionFilterForm(self.request.GET)
        if filter_form.is_valid():
            # Фильтрация по дате (с)
            date_from = filter_form.cleaned_data.get('date_from')
            if date_from:
                queryset = queryset.filter(date__gte=date_from)
                
            # Фильтрация по дате (по)
            date_to = filter_form.cleaned_data.get('date_to')
            if date_to:
                queryset = queryset.filter(date__lte=date_to)
                
            # Фильтрация по статусу
            status = filter_form.cleaned_data.get('status')
            if status:
                queryset = queryset.filter(status=status)
                
            # Фильтрация по типу транзакции
            transaction_type = filter_form.cleaned_data.get('transaction_type')
            if transaction_type:
                queryset = queryset.filter(transaction_type=transaction_type)
                
            # Фильтрация по категории
            category = filter_form.cleaned_data.get('category')
            if category:
                queryset = queryset.filter(category=category)
                
            # Фильтрация по подкатегории
            subcategory = filter_form.cleaned_data.get('subcategory')
            if subcategory:
                queryset = queryset.filter(subcategory=subcategory)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Добавляем форму фильтрации в контекст
        filter_form = TransactionFilterForm(self.request.GET)
        context['filter_form'] = filter_form
        
        # Рассчитываем общую сумму отфильтрованных транзакций
        queryset = self.get_queryset()
        
        # Общие суммы по типам транзакций
        income_sum = queryset.filter(transaction_type__name='Пополнение').aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        expense_sum = queryset.filter(transaction_type__name='Списание').aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        context.update({
            'income_sum': income_sum,
            'expense_sum': expense_sum,
            'balance': income_sum - expense_sum
        })
        
        return context


class TransactionCreateView(CreateView):
    """Представление для создания новой транзакции"""
    model = Transaction
    form_class = TransactionForm
    template_name = 'transaction/create.html'
    success_url = reverse_lazy('transaction_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Транзакция успешно создана.')
        return super().form_valid(form)


class TransactionUpdateView(UpdateView):
    """Представление для редактирования транзакции"""
    model = Transaction
    form_class = TransactionForm
    template_name = 'transaction/edit.html'
    success_url = reverse_lazy('transaction_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Транзакция успешно обновлена.')
        return super().form_valid(form)


class TransactionDeleteView(DeleteView):
    """Представление для удаления транзакции"""
    model = Transaction
    template_name = 'transaction/delete.html'
    success_url = reverse_lazy('transaction_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Транзакция успешно удалена.')
        return super().delete(request, *args, **kwargs)


# API для динамической загрузки категорий и подкатегорий
def get_categories(request):
    """API для получения категорий в зависимости от выбранного типа транзакции"""
    transaction_type_id = request.GET.get('transaction_type')
    if transaction_type_id:
        categories = Category.objects.filter(transaction_type_id=transaction_type_id).values('id', 'name')
        return JsonResponse(list(categories), safe=False)
    return JsonResponse([], safe=False)


def get_subcategories(request):
    """API для получения подкатегорий в зависимости от выбранной категории"""
    category_id = request.GET.get('category')
    if category_id:
        subcategories = Subcategory.objects.filter(category_id=category_id).values('id', 'name')
        return JsonResponse(list(subcategories), safe=False)
    return JsonResponse([], safe=False)


# Управление справочниками

class DirectoryListView(TemplateView):
    """Представление для страницы управления справочниками"""
    template_name = 'directory/list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'statuses': Status.objects.all(),
            'transaction_types': TransactionType.objects.all(),
            'categories': Category.objects.select_related('transaction_type').all(),
            'subcategories': Subcategory.objects.select_related('category').all()
        })
        return context


# Представления для управления статусами
class StatusCreateView(CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'directory/status_form.html'
    success_url = reverse_lazy('directory_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Статус успешно создан.')
        return super().form_valid(form)


class StatusUpdateView(UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'directory/status_form.html'
    success_url = reverse_lazy('directory_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Статус успешно обновлен.')
        return super().form_valid(form)


class StatusDeleteView(DeleteView):
    model = Status
    template_name = 'directory/delete.html'
    success_url = reverse_lazy('directory_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_type'] = 'статус'
        return context
    
    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except Exception as e:
            messages.error(request, f'Невозможно удалить статус. Он используется в транзакциях. {str(e)}')
            return redirect('directory_list')


# Представления для управления типами транзакций
class TransactionTypeCreateView(CreateView):
    model = TransactionType
    form_class = TransactionTypeForm
    template_name = 'directory/transaction_type_form.html'
    success_url = reverse_lazy('directory_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Тип транзакции успешно создан.')
        return super().form_valid(form)


class TransactionTypeUpdateView(UpdateView):
    model = TransactionType
    form_class = TransactionTypeForm
    template_name = 'directory/transaction_type_form.html'
    success_url = reverse_lazy('directory_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Тип транзакции успешно обновлен.')
        return super().form_valid(form)


class TransactionTypeDeleteView(DeleteView):
    model = TransactionType
    template_name = 'directory/delete.html'
    success_url = reverse_lazy('directory_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_type'] = 'тип транзакции'
        return context
    
    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except Exception as e:
            messages.error(request, f'Невозможно удалить тип транзакции. Он используется в транзакциях или категориях. {str(e)}')
            return redirect('directory_list')


# Представления для управления категориями
class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'directory/category_form.html'
    success_url = reverse_lazy('directory_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Категория успешно создана.')
        return super().form_valid(form)


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'directory/category_form.html'
    success_url = reverse_lazy('directory_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Категория успешно обновлена.')
        return super().form_valid(form)


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'directory/delete.html'
    success_url = reverse_lazy('directory_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_type'] = 'категорию'
        return context
    
    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except Exception as e:
            messages.error(request, f'Невозможно удалить категорию. Она используется в транзакциях или подкатегориях. {str(e)}')
            return redirect('directory_list')


# Представления для управления подкатегориями
class SubcategoryCreateView(CreateView):
    model = Subcategory
    form_class = SubcategoryForm
    template_name = 'directory/subcategory_form.html'
    success_url = reverse_lazy('directory_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Подкатегория успешно создана.')
        return super().form_valid(form)


class SubcategoryUpdateView(UpdateView):
    model = Subcategory
    form_class = SubcategoryForm
    template_name = 'directory/subcategory_form.html'
    success_url = reverse_lazy('directory_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Подкатегория успешно обновлена.')
        return super().form_valid(form)


class SubcategoryDeleteView(DeleteView):
    model = Subcategory
    template_name = 'directory/delete.html'
    success_url = reverse_lazy('directory_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_type'] = 'подкатегорию'
        return context
    
    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except Exception as e:
            messages.error(request, f'Невозможно удалить подкатегорию. Она используется в транзакциях. {str(e)}')
            return redirect('directory_list')