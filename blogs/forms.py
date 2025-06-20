#blog
from django import forms
from .models import Post

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


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['headline', 'content', 'image', 'publication']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Стилизация формы согласно post_form.html
        self.fields['headline'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите название статьи'
        })
        self.fields['content'].widget.attrs.update({
            'class': 'form-control',
            'rows': '3',
            'placeholder': 'Напишите содержание статьи'
        })
        self.fields['image'].widget.attrs.update({
            'class': 'form-control-file'
        })
        self.fields['publication'].widget.attrs.update({
            'class': 'form-check-input'
        })
        # Делаем поля обязательными, кроме publication
        self.fields['headline'].required = True
        self.fields['content'].required = True
        self.fields['image'].required = True

    def clean(self):
        cleaned_data = super().clean()
        headline = cleaned_data.get('headline', '').lower()
        content = cleaned_data.get('content', '').lower()

        for word in ban_words:
            if word in headline or word in content:
                raise forms.ValidationError(
                    f'Использование запрещенного слова "{word}" не допускается в названии или содержании статьи'
                )

        return cleaned_data