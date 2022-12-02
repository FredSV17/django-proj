from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render

from utils.pagination.pagination import make_paginator

from .models import Recipe


# Create your views here.
def home(request):
    recipes = Recipe.objects.filter(is_published=True,).order_by('-id')
    # get_list_or_404(Recipe.objects.filter(
    #    is_published=True,).order_by('-id'),)
    page_obj, pagination_range = make_paginator(request, recipes)
    return render(request, 'recipes/pages/home.html', context={
        'recipes': page_obj,
        'pages': pagination_range
    })


def search(request):
    search_query = request.GET.get('q', '').strip()
    if not search_query:
        raise Http404()
    # __contains = LIKE
    # __icontains = LIKE (case insensitive)
    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=search_query) | Q(
                description__icontains=search_query)
        ),
        is_published=True
    ).order_by('-id')

    page_obj, pagination_range = make_paginator(request, recipes)

    return render(request, 'recipes/pages/search.html', context={
        'page_title': f'"{search_query}" search ',
        'pages': pagination_range,
        'recipes': page_obj,
        'additional_query': f'&q={search_query}'
    })


def category(request, category_id):
    recipes = get_list_or_404(Recipe.objects.filter(
        is_published=True, category__id=category_id).order_by('-id'),)

    page_obj, pagination_range = make_paginator(request, recipes)
    return render(request, 'recipes/pages/category.html', context={
        'recipes': page_obj,
        'pages': pagination_range,
        'title': f'{recipes[0].category.name}  - Category |'
    })


def recipe(request, id):

    recipe = get_object_or_404(Recipe, pk=id, is_published=True)
    return render(request, 'recipes/pages/recipe_view.html', context={
        'recipe': recipe,
        'is_detail_page': True
    })
