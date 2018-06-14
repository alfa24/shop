from django import forms
from django.core.exceptions import ValidationError
from django.forms import modelformset_factory

from goods.models import Good, Category

NAME_ERROR_LIST = {"required": "Укажите название товара", "min_length": "Слишком короткое наименование",
                   "max_length": "Слишком длинное наименование"}


def validate_positive(value):
    if value < 0:
        raise ValidationError("Значение цены должно быть положительным!", code="invalid_positive")


class GoodForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['price'] <= cleaned_data['price_acc']:
            raise ValidationError("Цена с учетом скидки должна быть меньше цены!", code="invalid_discount")
        return cleaned_data

    class Meta:
        model = Good
        exclude = []
        widgets = {"content": forms.Textarea(attrs={"rows": 8, "cols": 10})}

    name = forms.CharField(label="Название", help_text="Должно быть уникальным", max_length=20,
                           error_messages=NAME_ERROR_LIST)
    description = forms.CharField(widget=forms.Textarea, label='Описание')
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория', empty_label=None,
                                      widget=forms.RadioSelect)
    price = forms.FloatField(label="Цена", validators=[validate_positive])
    in_stock = forms.BooleanField(label='Есть в наличии', required=False)

    # Добавляет класс в поля формы
    required_css_class = "required_good"
    error_css_class = "error_good"