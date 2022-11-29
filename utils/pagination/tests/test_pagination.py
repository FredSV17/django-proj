from unittest import TestCase

from utils.pagination.pagination import make_paginator_range


class TestPagination(TestCase):
    def test_pagination_returns_correct_range(self):
        pagination = make_paginator_range(
            list_pages=list(range(1, 21)),
            num_range=4,
            curr_page=1
        )
        self.assertEqual([1, 2, 3, 4], pagination['pagination'])

    def test_pagination_range_static_if_current_page_less_than_middle_of_range(self):
        pagination = make_paginator_range(
            list_pages=list(range(1, 21)),
            num_range=4,
            curr_page=1
        )
        self.assertEqual([1, 2, 3, 4], pagination['pagination'])

        pagination = make_paginator_range(
            list_pages=list(range(1, 21)),
            num_range=4,
            curr_page=2
        )
        self.assertEqual([1, 2, 3, 4], pagination['pagination'])

        # Page >= middle of range - should change range of pages
        pagination = make_paginator_range(
            list_pages=list(range(1, 21)),
            num_range=4,
            curr_page=3
        )
        self.assertEqual([2, 3, 4, 5], pagination['pagination'])

        # Another change of range
        pagination = make_paginator_range(
            list_pages=list(range(1, 21)),
            num_range=4,
            curr_page=4
        )
        self.assertEqual([3, 4, 5, 6], pagination['pagination'])

    def test_check_range_of_last_pages(self):

        pagination = make_paginator_range(
            list_pages=list(range(1, 21)),
            num_range=4,
            curr_page=19
        )
        self.assertEqual([17, 18, 19, 20], pagination['pagination'])

        # Next page - range should not change
        pagination = make_paginator_range(
            list_pages=list(range(1, 21)),
            num_range=4,
            curr_page=20
        )
        self.assertEqual([17, 18, 19, 20], pagination['pagination'])
