
import copy
import string

import pandas as pd

def appendRowToDF(row_dic,df):
      new_row = pd.DataFrame(row_dic, index=[0])
      return pd.concat([df.loc[:],new_row]).reset_index(drop=True)

def insert_new_column_in_df(df, col_name: string, col_array):
    df.insert(len(df.columns), col_name, col_array)

def add_column_relative_delta_perc_of_2_cols_in_dataframe(df, col1Name, relativeToColName,newColName):
    newColumn = (abs(df[col1Name] - df[relativeToColName]))/df[relativeToColName]*100
    # newColName = "relative-delta-percent_"+col1Name+"_wrt_"+relativeToColName
    insert_new_column_in_df(df,newColName,newColumn)
 
def add_column_absoluteValOfDeltaOf2cols_in_dataframe(df, col1Name, relativeToColName,newColName):
    newColumn = abs(df[col1Name] - df[relativeToColName])
    # newColName = "relative-delta-percent_"+col1Name+"_wrt_"+relativeToColName
    insert_new_column_in_df(df,newColName,newColumn)

def create_combined_dataframe_each_of_1_row(dataframes_array, col1Name, col2Name):
    #chatgbt generated, modified(named generic)
    combined_df = pd.DataFrame(columns=[col1Name, col2Name])
    for df in dataframes_array:
        row = df.iloc[0] 
        col1Value = row[col1Name]
        col2Value = row[col2Name]
        combined_df = combined_df.append({col1Name: col1Value, col2Name: col2Value}, ignore_index=True)
    return combined_df


def create_combined_dataframe_each_of_many_rows(dataframes_array, col1Name, col2Name):
    #chatgbt generated, modified(named generic)
    combined_df = pd.DataFrame(columns=[col1Name, col2Name])
    for df in dataframes_array:
         for _, row in df.iterrows():
            col1Value = row[col1Name]
            col2Value = row[col2Name]
            combined_df = combined_df.append({col1Name: col1Value, col2Name: col2Value}, ignore_index=True)
    return combined_df
