"""
    File name: Categorical_Encoding.py
    Author: Mayur Sonawane
    Date created: 8/26/2019
    Python Version: 3.7.4
"""

import pandas as pd
import pyarrow.parquet as pq
import json


def describe_df(df, op_describe_file, include=None):
    """
    Describe each column of pandas dataframe as per dtypes

    Parameters:
    df : (Pandas dataframe), include: list of dtypes or 'all' for all dtypes
    op_describe_file : output describe json file path
    include : which has values like ['category', np.number, np.object]
                or list of dtypes or 'all' for all dtypes
    Returns:
    raise an error in any
    """
    if include == 'all':
        desc_json = df_json(df.describe(include='all'))
    else:
        desc_json = df_json(df.describe(include=include))

    try:
        with open(op_describe_file, 'w') as fp:
            json.dump(desc_json, fp)
    except IOError as e:
        print("Error: while exporting descriptive_stats JSON", e)
        raise


def df_json(df_desc):
    """
    Convert & manipulate describe by updating JSON

    Parameters:
    pandas.core.frame.DataFrame

    Returns:
    list of JSON including column_name
    """
    op_json = json.loads(df_desc.to_json())
    for col_name in op_json:
        op_json[col_name]['column_name'] = col_name
    return op_json


def encode_dataframe(df):
    string_cols = get_columns_by_type(df, 'object')
    return pd.get_dummies(df, columns=string_cols)


def encode_df(df, op_encode_file):
    """
    encode each column of dataframe whose dtype is 'object'

    Parameters:
    df(Pandas dataframe): Dataframe to encode
    op_encode_file : ouput encoded file path

    Returns:
    df: Encoded pandas dataframe
    """
    try:
        encode_dataframe(df).to_parquet(op_encode_file)
    except IOError as e:
        print("Error: while exporting encoded parquet file ", e)
        raise


def get_columns_by_type(df, req_type):
    """
    get all columns of dataframe with provided dtypes

    Parameters:
    df : Pandas dataframe
    req_type: dtype

    Returns:
    list: list of columns
    """

    g = df.columns.to_series().groupby(df.dtypes).groups
    type_dict = {k.name: v for k, v in g.items()}
    return type_dict.get(req_type)


def read_file(file_path):
    """
    read all files and convert into pandas dataframe

    Parameters:
    file_path: file path

    Returns:
    df: Pandas Dataframe
    """
    return pq.read_table(file_path).to_pandas()

#
# def main():
#     print(len(sys.argv))
#     if len(sys.argv) != 3:
#         print("Usage: Encode Parquet file stats {}".format(sys.stderr))
#         exit(-1)
#
#     df = read_file(sys.argv[1])
#     input_file_name = os.path.splitext(os.path.basename(sys.argv[1]))[0]
#     output_describe_json = "{}/{}_description.json".format(sys.argv[2],input_file_name)
#     output_encode_parqute = "{}/{}_encoded.parquet".format(sys.argv[2], input_file_name)
#     describe_df(df, output_describe_json)
#     encode_df(df, output_encode_parqute)
#
# if __name__ == '__main__':
#     main()
