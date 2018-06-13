from django import forms

from goods.models import Good, Category


class GoodForm(forms.ModelForm):
    class Meta:
        model = Good
        exclude = []

    name = forms.CharField(label="Название", help_text="Должно быть уникальным")
    description = forms.CharField(widget=forms.Textarea, label='Описание')
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория', empty_label=None)
    in_stock = forms.BooleanField(initial=True, label='Есть в наличии')
