import numpy as np

def curve_number_aligner(curve_number_a, 
                         dict_prefix = 'cn_',
                         condition='drained'):
    """Implementation of the 'curve number aligner'. 
    see page 13 of Hawkins, R.H., Ward, T.J., Woodward, D.E., and Van Mullem, J.A., 2009, 
    Curve number hydrology: American Society of Civil Engineers, 106 p.

    Maximum theoretical value for an 'A' soil is 77. This is not enforced in the curve number aligner.

    Args:
        curve_number_a (numeric): SCS curve number for hydrologic soil group "A"
        dict_prefix (str, optional): dictionary prefix to use for returned dict. Defaults to 'cn_'.
        condition (str, optional): string indicating 'drained' or 'undrained' landuse. Defaults to 'drained'.

    Returns:
        dict: dictionary containing curve numbers for b-d and dual-classification soil groups
    """

    curve_number_b = np.round(min([37.8 + 0.622 * curve_number_a, 100.]), decimals=2)
    curve_number_c = np.round(min([58.9 + 0.411 * curve_number_a, 100.]), decimals=2)
    curve_number_d = np.round(min([67.2 + 0.328 * curve_number_a, 100.]), decimals=2)

    if condition == 'drained':
        curve_number_ad = curve_number_a
        curve_number_bd = curve_number_b
        curve_number_cd = curve_number_c
    else:
        curve_number_ad = curve_number_d
        curve_number_bd = curve_number_d
        curve_number_cd = curve_number_d

    result_dict= {f"{dict_prefix}a": curve_number_a,
                  f"{dict_prefix}b": curve_number_b,
                  f"{dict_prefix}c": curve_number_c,
                  f"{dict_prefix}d": curve_number_d,
                  f"{dict_prefix}ad": curve_number_ad,
                  f"{dict_prefix}bd": curve_number_bd,
                  f"{dict_prefix}cd": curve_number_cd}

    return result_dict