from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse
from recipes import views
from recipes.models import Category, Recipe


class RecipeViewsTest(TestCase):
    def test_create_recipe(self):
        self.make

    def test_recipe_home_views_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_view_loads_recipe(self):
        category = Category.objects.create(name='Categ')
        user = User.objects.create_user(
            first_name='John',
            last_name='Doe',
            username="jdoe",
            password='123456',
            email='jdoe@test.com')
        recipe = Recipe.objects.create(
            category=category,
            author=user,
            title='Recipe Title',
            description='Recipe description',
            slug='recipe-slug',
            preparation_time=11,
            preparation_time_unit='Minutes',
            servings=2,
            servings_unit='Servings',
            preparation_step='Recipe psteps',
            preparation_step_is_html=False,
            is_published=True
        )
        assert 1 == 1

    def test_recipe_home_no_recipes_found(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn('No recipes here', response.content.decode('utf-8'))

    def test_recipe_category_views_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_status_code_404_NOT_FOUND(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_views_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_views_returns_status_code_404_NOT_FOUND(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000}))
        self.assertEqual(response.status_code, 404)
