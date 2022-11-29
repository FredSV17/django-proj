import math


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
        'last_page_oor': curr_page < middle_range
    }
