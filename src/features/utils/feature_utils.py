# -*- coding: utf-8 -*-

def create_key_from_fields(*a):
    first = True
    key = ''
    for i in a:
        if first is True:
            key = i.astype(str)
            first = False
        else:
            key = key + '_' + i.astype(str)
    return key

def __range_standardize(value, range):
    dist_min = value
    dist_max = range - value
    return min(dist_min, dist_max)

def __is_adjacent(region_a, region_b):
    if region_a == 'W' or region_a == 'X':
        if region_b == 'X' or region_b == 'W':
            return True
    elif region_a == 'Y' or region_a == 'Z':
        if region_b == 'Y' or region_b == 'Z':
            return True
    return False

def __get_round(row):
    
    seed_a = row.Seed_x
    seed_b = row.Seed_y
    
    seed_a_region = seed_a[0:1]
    seed_b_region = seed_b[0:1]
        
    seed_a_int = int(seed_a[1:3]) - 1
    seed_b_int = int(seed_b[1:3]) - 1
    
    R_INIT = 15
    r_prev = 0

    # r = 15, 7, 3, 1
    if seed_a_region == seed_b_region:
        seed_a_standardized = seed_a_int
        seed_b_standardized = seed_b_int
        for i in range(1, 5):
            if i == 1:
                r = R_INIT
            else:
                r_prev = r
                r = (r_prev - 1) / 2
            seed_a_standardized = __range_standardize(seed_a_standardized, r)
            seed_b_standardized = __range_standardize(seed_b_standardized, r)
            
            if seed_a_standardized == seed_b_standardized:
                return i
    else:
        if __is_adjacent(seed_a_region, seed_b_region):
            return 5 #final 4
        else:
            return 6 ## finals

    return 0