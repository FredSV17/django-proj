
from django.forms import ValidationError
from parameterized import parameterized
from recipes.tests.test_recipe_base import Recipe, TestRecipeBase


class TestCategoryModel(TestRecipeBase):
    def setUp(self) -> None:
        self.category = self.make_category()
        return super().setUp()

    @parameterized.expand([
        ('name', 65)
    ])
    def test_recipe_check_char_limit(self, field, max_length):
        setattr(self.category, field, "A" * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.category.full_clean()

    def test_recipe_string_representation(self):
        needed = 'Testing Representation'
        self.category.name = needed
        self.category.full_clean()
        self.category.save()
        self.assertEqual(
            str(self.category), needed,
            msg=f'Category string representation must be '
                f'"{needed}" but "{str(self.category)}" was received.'
        )
