"""
    File name: feature_selection.py
    Author: Mayur Sonawane
    Date created: 8/26/2019
    Python Version: 3.7.4
"""

import pandas as pd
import json

from sklearn.ensemble import ExtraTreesClassifier

from .categorical_encoding import encode_dataframe


def get_columns_by_type(df, req_type):
    """
    get columns by type of data frame

    Parameters:
    df : data frame
    req_type : type of column like categorical, integer,

    Returns:
    df: Pandas data frame
    """
    g = df.columns.to_series().groupby(df.dtypes).groups
    type_dict = {k.name: v for k, v in g.items()}
    return type_dict.get(req_type)


def get_y_cols(data, clm):
    """
    get all columns which start with clm provided from pandas data frame data

    Parameters:
    data: Pandas data frame
    clm : string

    Returns:
    columns : list of columns
    """
    columns = [item for item in data.columns if item.startswith(clm)]
    # print("get cols------",columns)
    return columns


def top_features(df, output_regression_analysis_json, number_of_features=10):
    """
    get all features by considering every other column as a dependent variable
    with respect to all other columns considering independent variable

    Parameters:
    df: Pandas data frame
    output_regression_analysis_json : export path of the file
    number_of_features : integer

    """
    # print("number_of_features---", number_of_features)
    data = df.copy()
    all_columns = list(data.columns)
    data = encode_dataframe(data).fillna(0)
    op_json = {"Regression_analysis_results": []}

    for clm in all_columns:
        y_clms = get_y_cols(data, clm)
        data = data[[c for c in data if c not in y_clms] + y_clms]
        ind_col_length = len(y_clms)  # len(data.columns) - 1
        x = data.iloc[:, 0:ind_col_length]  # independent columns
        y = data.iloc[:, -1 * ind_col_length]  # dependent column
        model = ExtraTreesClassifier()
        try:
            model.fit(x, y)
        except:
            model.fit(x, y.astype('int'))

        #       #use inbuilt class feature_importances of tree based classifiers
        feat_importances = pd.Series(model.feature_importances_, index=x.columns)
        o_j = dict()
        o_j["dependent_column_name"] = clm
        o_j["regression_details"] = []
        for key, value in json.loads(feat_importances.sort_values(ascending=False).to_json(orient='index')).items():
            o_j["regression_details"].append({"independent_column_name": key, "weight": value})
        op_json["Regression_analysis_results"].append(o_j)

    with open(output_regression_analysis_json,
              'w') as outfile:
        json.dump(op_json, outfile)

    print("Done with feature selection")
