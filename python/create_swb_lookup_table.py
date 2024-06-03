import argparse
import tomli
from pathlib import Path
from curve_number_aligner import curve_number_aligner
from net_infiltration_aligner import net_infiltration_aligner
from root_zone_aligner import root_zone_aligner
import numpy as np
from collections import defaultdict
from combine_dicts import combine_dicts, combine_lists
import pandas as pd

parser = argparse.ArgumentParser(
    description='Given a list of TOML files, process the parameter values and create a swb lookup table')
parser.add_argument('filelist', nargs='+')
toml_list = parser.parse_args().filelist

# establish base directory where this script is being executed
cwd = Path.cwd()

toml_dict = {}

# open up all of the TOML files; combine them into a single dictionary
for toml_file in toml_list:
    with open(toml_file, "rb") as f:
        temp_dict = tomli.load(f)
    toml_dict = combine_dicts(toml_dict, temp_dict)

# parse the 'categories' (e.g. 'small_grains') and landuse codes from dict
lu_categories = sorted(list(toml_dict['lu'].keys())) 

lu_codes = []
lu_descriptions = []
lu_full_category_list = []
for lu in lu_categories:
    lu_code_list = toml_dict['lu'][lu]['lu_code']
    lu_category_list = []
    for n in range(len(lu_code_list)):
        lu_category_list.append(lu)
    lu_full_category_list = lu_full_category_list + lu_category_list
    lu_codes = combine_lists(lu_codes, toml_dict['lu'][lu]['lu_code'])
    lu_descriptions = combine_lists(lu_descriptions, toml_dict['lu'][lu]['description'])
#lu_codes = sorted(lu_codes)

df = pd.DataFrame({'lu_code': lu_codes, 'lu_description': lu_descriptions,
                  'lu_category': lu_full_category_list,
                  'cn_1': np.float64}).sort_values('lu_code')

for lu in lu_categories:
    cn = toml_dict['lu'][lu]['curve_number']
    max_net_infil = toml_dict['lu'][lu]['max_net_infiltration']
    cn_condition = toml_dict['lu'][lu]['curve_number_condition']
    cn_dict = curve_number_aligner(cn, condition=cn_condition)
    ni_dict = net_infiltration_aligner(max_net_infil)
    df.loc[df.lu_category==lu, 'cn_1'] = cn_dict['cn_a']
    df.loc[df.lu_category==lu, 'cn_2'] = cn_dict['cn_b']
    df.loc[df.lu_category==lu, 'cn_3'] = cn_dict['cn_c']
    df.loc[df.lu_category==lu, 'cn_4'] = cn_dict['cn_d']
    df.loc[df.lu_category==lu, 'cn_5'] = cn_dict['cn_ad']
    df.loc[df.lu_category==lu, 'cn_6'] = cn_dict['cn_bd']
    df.loc[df.lu_category==lu, 'cn_7'] = cn_dict['cn_cd']

    df.loc[df.lu_category==lu, 'max_net_infil_1'] = ni_dict['max_net_infil_a']
    df.loc[df.lu_category==lu, 'max_net_infil_2'] = ni_dict['max_net_infil_b']
    df.loc[df.lu_category==lu, 'max_net_infil_3'] = ni_dict['max_net_infil_c']
    df.loc[df.lu_category==lu, 'max_net_infil_4'] = ni_dict['max_net_infil_d']
    df.loc[df.lu_category==lu, 'max_net_infil_5'] = ni_dict['max_net_infil_ad']
    df.loc[df.lu_category==lu, 'max_net_infil_6'] = ni_dict['max_net_infil_bd']
    df.loc[df.lu_category==lu, 'max_net_infil_7'] = ni_dict['max_net_infil_cd']

    df.loc[df.lu_category==lu, 'growing_season_interception'] = toml_dict['lu'][lu]['growing_season_interception']
    df.loc[df.lu_category==lu, 'nongrowing_season_interception'] = toml_dict['lu'][lu]['nongrowing_season_interception']

    df.loc[df.lu_category==lu, 'kcb_ini'] = toml_dict['lu'][lu]['kcb']['ini']
    df.loc[df.lu_category==lu, 'kcb_mid'] = toml_dict['lu'][lu]['kcb']['mid']
    df.loc[df.lu_category==lu, 'kcb_end'] = toml_dict['lu'][lu]['kcb']['end']
    df.loc[df.lu_category==lu, 'kcb_min'] = toml_dict['lu'][lu]['kcb']['min']
