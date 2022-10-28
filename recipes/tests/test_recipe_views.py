from django.contrib.auth.models import User
from django.urls import resolve, reverse
from recipes import views
from recipes.models import Category, Recipe
from recipes.tests.test_recipe_base import TestRecipeBase


class RecipeViewsTest(TestRecipeBase):

    # TEST HOME PAGE
    def test_recipe_home_views_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_omits_recipe_if_not_published(self):
        """
            Test if recipes that are not published don't appear
        """

        # Create recipe that is not published
        self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:home'))

        # Should not appear
        self.assertIn('No recipes here', response.content.decode('utf-8'))

    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_view_loads_recipe(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        context = response.content.decode('utf-8')
        recipes = response.context['recipes']
        self.assertIn('Recipe Title', context)
        self.assertIn('11 Minutes', context)
        self.assertIn('2 Servings', context)
        self.assertEqual(len(recipes), 1)

    def test_recipe_home_no_recipes_found(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn('No recipes here', response.content.decode('utf-8'))

    def test_recipe_category_view_loads_recipe(self):
        title = 'Category test - one recipe only'

        # Create recipe for test
        self.make_recipe(title=title)

        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1}))
        context = response.content.decode('utf-8')
        self.assertIn(title, context)

    # TEST CATEGORY PAGE

    def test_recipe_category_view_omits_recipe_if_not_published(self):
        """
            Test if recipes that are not published don't appear
        """

        # Create recipe that is not published
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': recipe.category.id}))

        # Should not appear
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_views_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_status_code_404_NOT_FOUND(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertEqual(response.status_code, 404)

    # TEST DETAIL PAGE
    def test_recipe_detail_views_returns_status_code_404_NOT_FOUND(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_view_omits_recipe_if_not_published(self):
        """
            Test if recipes that are not published don't appear
        """

        # Create recipe that is not published
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': recipe.id}))

        # Should not appear
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_views_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_loads_correct_recipe(self):
        title = 'Detail test - One recipe only'

        # Create recipe for test
        self.make_recipe(title=title)

        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1}))
        context = response.content.decode('utf-8')
        self.assertIn(title, context)
