from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.base import ContextMixin, TemplateView
from django.views.generic.edit import ProcessFormView, CreateView, UpdateView, DeleteView, FormMixin

from goods.forms import GoodForm
from goods.models import Category, Good


class CategoryListMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cats'] = Category.objects.order_by('name')
        return context


# class GoodListView(TemplateView):
#     template_name = 'index.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         try:
#             page_num = self.request.GET['page']
#         except KeyError:
#             page_num = 1
#
#         context['cats'] = Category.objects.order_by('name')
#
#         if not kwargs['cat_id']:
#             context['category'] = Category.objects.first()
#         else:
#             context['category'] = Category.objects.get(pk=kwargs['cat_id'])
#         paginator = Paginator(Good.objects.filter(
#             category=context['category']).order_by('name'), 1)
#
#         try:
#             context['goods'] = paginator.page(page_num)
#         except InvalidPage:
#             context['goods'] = paginator.page(1)
#         return context


class GoodListView(ListView, CategoryListMixin):
    template_name = 'index.html'
    paginate_by = 5
    cat = None

    def get(self, request, *args, **kwargs):
        # определяем категорию из URL
        if not kwargs['cat_id']:
            self.cat = Category.objects.first()
        else:
            self.cat = Category.objects.get(pk=kwargs['cat_id'])
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        # устанавуливаем список товаров
        return Good.objects.filter(category=self.cat).order_by('name')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['category'] = self.cat
        # так же в шаблон передается
        # paginator - пагинация
        # page_obj - объект класса Page, представляющий текущую страницу
        # is_paginated - Если задействована пагинация
        # object_list - qs Список записей для вывода

        return context


# class GoodDetailView(TemplateView):
#     template_name = 'good.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         try:
#             context['pn'] = self.request.GET['page']
#         except KeyError:
#             context['pn'] = 1
#
#         context['cats'] = Category.objects.all().order_by('name')
#         try:
#             context['good'] = Good.objects.get(pk=kwargs['good_id'])
#         except Good.DoesNotExist:
#             raise Http404
#
#         return context


class GoodDetailView(DetailView, CategoryListMixin):
    template_name = 'good.html'
    model = Good
    pk_url_kwarg = 'good_id'  # переменная, которая передается в url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # номер текущей страницы
        try:
            context['pn'] = self.request.GET['page']
        except KeyError:
            context['pn'] = 1

        # автоматически предается в шаблон
        # object, good - объект выводимой записи

        return context


class GoodEditMixin(CategoryListMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["pn"] = self.request.GET['page']
        except KeyError:
            context['pn'] = '1'
        return context


class GoodEditView(ProcessFormView):
    def post(self, request, *args, **kwargs):
        try:
            pn = request.GET['page']
        except KeyError:
            pn = '1'
        self.success_url = self.success_url + '?page=' + pn
        return super().post(request, *args, **kwargs)


class GoodCreate(CreateView, GoodEditMixin):
    model = Good
    form_class = GoodForm
    template_name = "good_add.html"

    # fields = [field.name for field in model._meta.fields]

    def get(self, request, *args, **kwargs):
        if self.kwargs['cat_id']:
            self.initial['category'] = Category.objects.get(pk=self.kwargs['cat_id'])
        self.initial['in_stock'] = request.session.get('in_stock', True)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.success_url = reverse('index', kwargs={'cat_id': Category.objects.get(pk=self.kwargs['cat_id']).id})
        request.session['in_stock'] = request.POST.get('in_stock', True)
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(pk=self.kwargs['cat_id'])
        return context


class GoodUpdate(SuccessMessageMixin, UpdateView, GoodEditMixin, GoodEditView):
    model = Good
    form_class = GoodForm
    template_name = "good_edit.html"
    pk_url_kwarg = "good_id"
    # fields = [field.name for field in model._meta.fields]
    # добавляем сообщение в request
    #  переопределяем из SuccessMessageMixin
    success_message = "Товар успешно обновлен."

    def post(self, request, *args, **kwargs):
        self.success_url = reverse('index', kwargs={'cat_id': Good.objects.get(pk=self.kwargs['good_id']).category.id})
        return super().post(request, *args, **kwargs)


class GoodDelete(DeleteView, GoodEditMixin, GoodEditView):
    model = Good
    template_name = "good_delete.html"
    pk_url_kwarg = "good_id"
    fields = [field.name for field in model._meta.fields]

    def post(self, request, *args, **kwargs):
        self.success_url = reverse('index', kwargs={'cat_id': Good.objects.get(pk=self.kwargs['good_id']).category.id})
        # добавляем сообщение в request
        messages.add_message(request, messages.SUCCESS, "Товар успешно удален.")
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['good'] = Good.objects.get(pk=self.kwargs['good_id'])
        return context
