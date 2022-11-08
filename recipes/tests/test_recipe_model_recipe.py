
from django.forms import ValidationError
from parameterized import parameterized
from recipes.tests.test_recipe_base import Recipe, TestRecipeBase


class TestRecipeModel(TestRecipeBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_no_defaults(self):
        recipe = Recipe(
            category=self.make_category(name='Test Default Category'),
            author=self.make_author(username='newuser'),
            title='Recipe Title',
            description='Recipe Description',
            slug='new-recipe',
            preparation_time=10,
            preparation_time_unit='Minutes',
            servings=5,
            servings_unit='Servings',
            preparation_step='Recipe Preparation Steps',
        )
        recipe.full_clean()
        recipe.save()
        return recipe

    @parameterized.expand([
        ('title', 65),
        ('description', 165),
        ('preparation_time_unit', 65),
        ('servings_unit', 65)
    ])
    def test_recipe_check_char_limit(self, field, max_length):
        setattr(self.recipe, field, "A" * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_preparation_steps_html_check_default_false(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(recipe.preparation_step_is_html)

    def test_recipe_preparation_is_published_check_default_false(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(recipe.is_published)

    def test_recipe_string_representation(self):
        needed = 'Testing Representation'
        self.recipe.title = needed
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(
            str(self.recipe), needed,
            msg=f'Recipe string representation must be '
                f'"{needed}" but "{str(self.recipe)}" was received.'
        )
