from django.http import Http404
from django.shortcuts import render
from django.core.paginator import Paginator, InvalidPage

from .models import Category, Good


def index(request, cat_id=None):
    try:
        page_num = request.GET['page']
    except KeyError:
        page_num = 1

    cats = Category.objects.all().order_by('name')

    if not cat_id:
        cat = Category.objects.first()
    else:
        cat = Category.objects.get(pk=cat_id)

    paginator = Paginator(Good.objects.filter(
        category=cat).order_by('name'), 5)

    try:
        goods = paginator.page(page_num)
    except InvalidPage:
        goods = paginator.page(1)

    print(goods)

    return render(request, 'index.html', context={'cats': cats,
                                                  'goods': goods,
                                                  'category': cat}
                  )


def good(request, good_id):
    try:
        page_num = request.GET['page']
    except KeyError:
        page_num = 1

    cats = Category.objects.all().order_by('name')
    try:
        good = Good.objects.get(pk=good_id)
    except Good.DoesNotExist:
        raise Http404

    return render(request, 'good.html', context={'good': good, 'cats': cats, 'pn': page_num})
