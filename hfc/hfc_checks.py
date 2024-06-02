# Data Quality checks
import pandas as pd


# Checking for duplicates in respondent id
def duplicates(
    df: pd.DataFrame, respondent_id, surveyor_id, date, start_time, end_time
):
    df["dup_id"] = df.duplicated(subset=[respondent_id])
    data_dup = df[df["dup_id"] == True]
    results = data_dup[[respondent_id, surveyor_id, date, start_time, end_time]]
    print(results)
    return results
