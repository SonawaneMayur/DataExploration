"""
    File name: analyze.py
    Author: Mayur Sonawane
    Date created: 8/26/2019
    Python Version: 3.7.4
"""

import sys
import os

from functions.categorical_encoding import read_file, describe_df, encode_df
from functions.feature_selection import top_features
from functions.utils import get_logger


logger = get_logger(__name__)

def main():
    print(len(sys.argv))
    if len(sys.argv) != 3:
        print("Usage: Parquet file stats {}".format(sys.stderr))
        exit(-1)

    df = read_file(sys.argv[1])
    input_file_name = os.path.splitext(os.path.basename(sys.argv[1]))[0]
    output_describe_json = "{}/{}_descriptive_stats.json".format(sys.argv[2], input_file_name)
    output_encode_parqute = "{}/{}_encoded.parquet".format(sys.argv[2], input_file_name)
    output_regression_analysis_json = "{}/{}_regression_analysis.json".format(sys.argv[2], input_file_name)
    describe_df(df, output_describe_json)
    logger.info('descriptive Stats gets generated at {}'.format(output_describe_json))
    encode_df(df, output_encode_parqute)
    logger.info('categorical encoding at {}'.format(output_encode_parqute))
    top_features(df, output_regression_analysis_json)
    logger.info('regression analysis at {}'.format(output_regression_analysis_json))


if __name__ == '__main__':
    main()
