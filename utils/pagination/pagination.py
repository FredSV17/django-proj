import math

from django.core.paginator import Paginator


def make_paginator_range(list_pages, num_range, curr_page):
    middle_range = math.ceil(num_range / 2)
    start_range = curr_page - middle_range
    stop_range = curr_page + middle_range

    if start_range < 0:
        start_range_offset = abs(start_range)
        start_range = 0
        stop_range += start_range_offset

    num_total_pages = len(list_pages)
    if stop_range > num_total_pages:
        stop_range_offset = abs(stop_range - num_total_pages)
        stop_range = num_total_pages
        start_range -= stop_range_offset

    pagination = list_pages[start_range:stop_range]

    return {
        'pagination': pagination,
        'num_range': num_range,
        'list_pages': list_pages,
        'curr_page': curr_page,
        'total_pages': num_total_pages,
        'start_range': start_range,
        'stop_range': stop_range,
        'first_page_oor': curr_page > middle_range,
        'last_page_oor': curr_page < num_total_pages - middle_range
    }


def make_paginator(request, queryset, per_page=9, num_range=5):
    try:
        curr_page = int(request.GET.get('page', '1'))
    except ValueError:
        curr_page = 1

    paginator = Paginator(queryset, per_page)
    page_obj = paginator.get_page(curr_page)

    pagination_range = make_paginator_range(
        paginator.page_range,
        num_range,
        curr_page
    )
    return page_obj, pagination_range
