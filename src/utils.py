import pandas as pd

def get_month_list_in_interval(start_date, end_date):
    interval_to_fetch = pd.date_range(start_date, end_date, freq='MS')
    return interval_to_fetch



def ensure_folder_exists(folder_path):
    import os
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    # while check==0 or num_try < max_tries:
    #     if not os.path.exists(folder_path):
    #         os.makedirs(folder_path)
    #     else:
    #         check=1
    #     num_try+=1


def get_start_end_dates(start_date=False, end_date=False):
    from datetime import datetime, timedelta
    import pytz

    dt_today = datetime.now(tz=pytz.timezone('America/Sao_Paulo'))
    if dt_today.day < 12:
        start_dt_str = (dt_today - timedelta(days=20)).replace(day=1, hour=0, minute=0, microsecond=0).strftime('%Y-%m-%d')
    else:
        start_dt_str = dt_today.replace(day=1, hour=0, minute=0, microsecond=0).strftime('%Y-%m-%d')
        
    end_dt_str = dt_today.replace(day=1, hour=0, minute=0, microsecond=0).strftime('%Y-%m-%d')

    if start_date:
        start_dt_str = start_date
    if end_date:
        end_dt_str = end_date

    print(f"Start: {start_dt_str}\nEnd: {end_dt_str}")
    return start_dt_str, end_dt_str