# Data Quality checks
import pandas as pd


# Checking for duplicates in respondent id
def duplicates(df: pd.DataFrame, id_column: int):
    df["dup_id"] = df.duplicated(subset=df.columns[0])
    data_dup = df[df["dup_id"] == True]
    print(data_dup.iloc[:, :10])
