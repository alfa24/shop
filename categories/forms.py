from django.forms import modelformset_factory
from django import forms

from categories.models import Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = []

    name = forms.CharField(label="Название", help_text="Должно быть уникальным")


CategoriesFormset = modelformset_factory(Category, form=CategoryForm, max_num=10, validate_max=True, can_delete=True,
                                         can_order=True)
