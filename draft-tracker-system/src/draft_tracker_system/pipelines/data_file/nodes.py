import pandas as pd 

def clean_file(df:pd.DataFrame):
    
    start_col = df.columns.get_loc("# GP")
    df = df.dropna(subset=df.columns[start_col:])

    return df

