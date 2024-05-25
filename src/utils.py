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