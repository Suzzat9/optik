# Data Quality checks
import pandas as pd
from datetime import datetime
from datetime import timedelta


# Checking for duplicates in respondent id
def duplicates(
    df: pd.DataFrame, respondent_id, surveyor_id, date, start_time, end_time
):
    df=df.rename(columns = {respondent_id:'respondent_id', 
                            surveyor_id: 'surveyor_id', 
                            date: 'date',
                            start_time: 'start_time',
                            end_time: 'end_time'})
    df["dup_id"] = df.duplicated(subset=['respondent_id'])
    df['date'] = pd.to_datetime(df['date'], unit='ms').dt.date
    # df['start_time'] = pd.to_datetime(df['start_time'], unit='ms').dt.time
    # df['end_time'] = pd.to_datetime(df['end_time'], unit='ms').dt.time
    data_dup = df[df["dup_id"] == True]
    results = data_dup[['respondent_id', 'surveyor_id', 'date', 'start_time', 'end_time']]

    
    #print(results)
    return results


def short_long_surveys(df:pd.DataFrame, respondent_id, surveyor_id, date, 
                       start_time, end_time, min_duration, max_duration):
    '''
    Get the short and long surveys from the data
    '''
    
    df=df.rename(columns = {respondent_id:'respondent_id', 
                            surveyor_id: 'surveyor_id', 
                            date: 'date',
                            start_time: 'start_time',
                            end_time: 'end_time'})
    
    results = df[['respondent_id', 'surveyor_id', 'date', 'start_time', 'end_time']]

    results['start_time'] = results['start_time'].apply(lambda t: datetime.combine(datetime.today(), t))
    results['end_time'] = results['end_time'].apply(lambda t: datetime.combine(datetime.today(), t))

    results["duration"] = results['end_time'] - results['start_time']
    #print(results)
    #results['duration'] = results['duration'] // 60000  # Convert duration to minutes

    max_duration_timedelta = timedelta(minutes=max_duration)
    min_duration_timedelta = timedelta(minutes=min_duration)

    results_long = results[results["duration"] >= max_duration_timedelta]
    results_short = results[results["duration"] <= min_duration_timedelta]

    df['date'] = pd.to_datetime(df['date'], unit='ms').dt.date
   
    

    return results_long, results_short

def prep_categorical_variable(df: pd.DataFrame, var: str):
    '''
    prepping categorical vars for plotting
    '''

    df_count = df.groupby([var]).size().reset_index(name='value')

    return df_count.to_json(orient='records')


def get_vars(variables:str):
    '''
    Return array of variables to plot
    '''
    
    return variables.split(',') 


