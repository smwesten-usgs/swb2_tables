import numpy as np

def root_zone_aligner(root_zone_depth_a, 
                      dict_prefix = 'rz_',
                      root_zone_factors=[1.25, 1.0, 0.666],
                      condition='drained'):
    """
    Implementation of a method for enforcing stucture on root zone depths. The 
    ratios applied between the soil groups roughly follows the relations given in 
    table 10 of Thornthwaite and Mather (1957). In that publication, there is a
    suggestion that the maximum rooting depth is associated with the 'B' soil group,
    with the rooting depth for 'C' and 'D' soils significantly smaller than those
    for the 'B' soil group.

    Args:
        root_zone_depth_a (_type_): _description_
        dict_prefix (str, optional): _description_. Defaults to 'rz_'.
        root_zone_factors (list, optional): _description_. Defaults to [1.25, 1.0, 0.666].
        condition (str, optional): _description_. Defaults to 'drained'.

    Returns:
        dict: dictionary containing rooting depths for b-d and dual-classification soil groups
    """

    rz_b = np.round(root_zone_depth_a * 1.25, decimals=2)
    rz_c = np.round(root_zone_depth_a, decimals=2)
    rz_d = np.round(root_zone_depth_a * 0.666, decimals=2)

    if condition == 'drained':
        rz_ad = root_zone_depth_a
        rz_bd = rz_b
        rz_cd = rz_c
    else:
        rz_ad = rz_d
        rz_bd = rz_d
        rz_cd = rz_d

    result_dict= {f"{dict_prefix}a": root_zone_depth_a,
                  f"{dict_prefix}b": rz_b,
                  f"{dict_prefix}c": rz_c,
                  f"{dict_prefix}d": rz_d,
                  f"{dict_prefix}ad": rz_ad,
                  f"{dict_prefix}bd": rz_bd,
                  f"{dict_prefix}cd": rz_cd}

    return result_dict