# catalog
from django import forms
from catalog.models import Product

ban_words = [
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'category', 'image', 'published']

        widgets = {
            'owner': forms.HiddenInput()  # Скрываем поле владельца в форме
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Применяем классы стилей из add_product.html
        for field_name, field in self.fields.items():
            if field_name == 'description':
                field.widget.attrs.update({
                    'class': 'form-control',
                    'rows': '3'
                })
            elif field_name == 'category':
                field.widget.attrs.update({
                    'class': 'form-select'
                })
            elif field_name == 'image':
                field.widget.attrs.update({
                    'class': 'form-control'
                })
            elif field_name == 'published':
                field.widget.attrs.update({
                    'class': 'form-control'
                })
            else:
                field.widget.attrs.update({
                    'class': 'form-control'
                })
            field.required = True

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise forms.ValidationError('Цена не может быть отрицательной')
        return price

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name', '').lower()
        description = cleaned_data.get('description', '').lower()

        for word in ban_words:
            if word in name or word in description:
                raise forms.ValidationError(
                    f'Использование запрещенного слова "{word}" не допускается в названии или описании продукта'
                )

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:  # Устанавливаем владельца если пользователь передан
            instance.owner = self.user
        if commit:
            instance.save()
        return instance
