from django import forms
from django.core.exceptions import ValidationError
from .models import Transaction, Status, TransactionType, Category, Subcategory


class StatusForm(forms.ModelForm):
    """Форма для создания и редактирования статусов"""
    class Meta:
        model = Status
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }


class TransactionTypeForm(forms.ModelForm):
    """Форма для создания и редактирования типов транзакций"""
    class Meta:
        model = TransactionType
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }


class CategoryForm(forms.ModelForm):
    """Форма для создания и редактирования категорий"""
    class Meta:
        model = Category
        fields = ['name', 'transaction_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'transaction_type': forms.Select(attrs={'class': 'form-select'})
        }


class SubcategoryForm(forms.ModelForm):
    """Форма для создания и редактирования подкатегорий"""
    class Meta:
        model = Subcategory
        fields = ['name', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'})
        }


class TransactionForm(forms.ModelForm):
    """Форма для создания и редактирования транзакций"""
    class Meta:
        model = Transaction
        fields = ['date', 'status', 'transaction_type', 'category', 'subcategory', 'amount', 'comment']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'transaction_type': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'subcategory': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Если форма инициализирована с данными, заполняем поля правильными значениями
        if self.instance and self.instance.pk:
            # Если это редактирование существующей транзакции
            self.fields['category'].queryset = Category.objects.filter(
                transaction_type=self.instance.transaction_type
            )
            self.fields['subcategory'].queryset = Subcategory.objects.filter(
                category=self.instance.category
            )
        else:
            # Если это новая транзакция, изначально ограничиваем выбор
            self.fields['category'].queryset = Category.objects.none()
            self.fields['subcategory'].queryset = Subcategory.objects.none()
        
            # Если есть начальные данные для типа транзакции, загружаем категории
            if 'transaction_type' in self.data:
                try:
                    transaction_type_id = int(self.data.get('transaction_type'))
                    self.fields['category'].queryset = Category.objects.filter(
                        transaction_type_id=transaction_type_id
                    )
                except (ValueError, TypeError):
                    pass
                    
            # Если есть начальные данные для категории, загружаем подкатегории
            if 'category' in self.data:
                try:
                    category_id = int(self.data.get('category'))
                    self.fields['subcategory'].queryset = Subcategory.objects.filter(
                        category_id=category_id
                    )
                except (ValueError, TypeError):
                    pass
    
    def clean(self):
        """Валидация логических зависимостей между полями"""
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get('transaction_type')
        category = cleaned_data.get('category')
        subcategory = cleaned_data.get('subcategory')
        
        if transaction_type and category and category.transaction_type != transaction_type:
            self.add_error('category', 'Категория должна соответствовать выбранному типу транзакции')
        
        if category and subcategory and subcategory.category != category:
            self.add_error('subcategory', 'Подкатегория должна соответствовать выбранной категории')
        
        return cleaned_data


class TransactionFilterForm(forms.Form):
    """Форма для фильтрации транзакций"""
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    transaction_type = forms.ModelChoiceField(
        queryset=TransactionType.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    subcategory = forms.ModelChoiceField(
        queryset=Subcategory.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Изначально подкатегории и категории пустые
        self.fields['category'].queryset = Category.objects.none()
        self.fields['subcategory'].queryset = Subcategory.objects.none()
        
        # Если есть данные в форме (POST или GET запрос с параметрами)
        if args:
            data = args[0]
            # Если выбран тип транзакции, фильтруем категории
            if 'transaction_type' in data and data['transaction_type']:
                try:
                    transaction_type_id = int(data['transaction_type'])
                    self.fields['category'].queryset = Category.objects.filter(
                        transaction_type_id=transaction_type_id
                    )
                except (ValueError, TypeError):
                    self.fields['category'].queryset = Category.objects.all()
            else:
                self.fields['category'].queryset = Category.objects.all()
                
            # Если выбрана категория, фильтруем подкатегории
            if 'category' in data and data['category']:
                try:
                    category_id = int(data['category'])
                    self.fields['subcategory'].queryset = Subcategory.objects.filter(
                        category_id=category_id
                    )
                except (ValueError, TypeError):
                    self.fields['subcategory'].queryset = Subcategory.objects.all()
            else:
                self.fields['subcategory'].queryset = Subcategory.objects.all()