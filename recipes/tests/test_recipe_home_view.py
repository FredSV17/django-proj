from django.urls import resolve, reverse
from recipes import views
from recipes.tests.test_recipe_base import TestRecipeBase


class RecipeHomeViewTest(TestRecipeBase):
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
