from django.urls import resolve, reverse
from recipes import views
from recipes.tests.test_recipe_base import TestRecipeBase


class RecipeCategoryViewTest(TestRecipeBase):
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
