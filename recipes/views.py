from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render

from .models import Recipe


# Create your views here.
def home(request):
    recipes = Recipe.objects.filter(is_published=True,).order_by('-id')
    # get_list_or_404(Recipe.objects.filter(
    #    is_published=True,).order_by('-id'),)
    return render(request, 'recipes/pages/home.html', context={
        'recipes': recipes
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

    return render(request, 'recipes/pages/search.html', context={
        'page_title': f'"{search_query}" search ',
        'recipes': recipes
    })


def category(request, category_id):
    recipes = get_list_or_404(Recipe.objects.filter(
        is_published=True, category__id=category_id).order_by('-id'),)
    return render(request, 'recipes/pages/category.html', context={
        'recipes': recipes,
        'title': f'{recipes[0].category.name}  - Category |'
    })


def recipe(request, id):

    recipe = get_object_or_404(Recipe, pk=id, is_published=True)
    return render(request, 'recipes/pages/recipe_view.html', context={
        'recipe': recipe,
        'is_detail_page': True
    })
