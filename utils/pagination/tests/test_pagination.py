from unittest import TestCase

from utils.pagination.pagination import make_paginator_range


class TestPagination(TestCase):
    def test_pagination_returns_correct_range(self):
        pagination = make_paginator_range(
            list_pages=list(range(1, 21)),
            num_range=4,
            curr_page=1
        )
        self.assertEqual([1, 2, 3, 4], pagination)

    def test_pagination_range_static_if_current_page_less_than_middle_of_range(self):
        ...
