from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone


class Status(models.Model):
    """Модель для статусов транзакций (Бизнес, Личное, Налог и т.д.)"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    
    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class TransactionType(models.Model):
    """Модель для типов транзакций (Пополнение, Списание и т.д.)"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    
    class Meta:
        verbose_name = "Тип транзакции"
        verbose_name_plural = "Типы транзакций"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Category(models.Model):
    """
    Модель для категорий транзакций (Инфраструктура, Маркетинг и т.д.)
    Привязана к типу транзакции.
    """
    name = models.CharField(max_length=100, verbose_name="Название")
    transaction_type = models.ForeignKey(
        TransactionType, 
        on_delete=models.CASCADE, 
        related_name='categories',
        verbose_name="Тип транзакции"
    )
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']
        unique_together = ['name', 'transaction_type']
    
    def __str__(self):
        return f"{self.name} ({self.transaction_type})"


class Subcategory(models.Model):
    """
    Модель для подкатегорий транзакций (VPS, Proxy, Farpost, Avito и т.д.)
    Привязана к категории.
    """
    name = models.CharField(max_length=100, verbose_name="Название")
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='subcategories',
        verbose_name="Категория"
    )
    
    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        ordering = ['name']
        unique_together = ['name', 'category']
    
    def __str__(self):
        return f"{self.name} ({self.category})"


class Transaction(models.Model):
    """Модель для записей о движении денежных средств"""
    date = models.DateField(default=timezone.now, verbose_name="Дата")
    status = models.ForeignKey(
        Status, 
        on_delete=models.PROTECT,
        verbose_name="Статус"
    )
    transaction_type = models.ForeignKey(
        TransactionType, 
        on_delete=models.PROTECT,
        verbose_name="Тип"
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.PROTECT,
        verbose_name="Категория"
    )
    subcategory = models.ForeignKey(
        Subcategory, 
        on_delete=models.PROTECT,
        verbose_name="Подкатегория"
    )
    amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name="Сумма (руб.)"
    )
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Время обновления")
    
    class Meta:
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"
        ordering = ['-date', '-created_at']
    
    def __str__(self):
        return f"{self.date} | {self.transaction_type} | {self.category} | {self.amount} руб."