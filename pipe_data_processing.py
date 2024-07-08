from datetime import datetime
import time

from src.pipelines import pipeline_data_collection, pipeline_data_processing
from src.utils import get_start_end_dates

print(f"# Starting data pipeline at {datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}\n")

id_deputados_to_fetch = [220526, 178873, 220527, 220530, 160517, 
                         220528, 204356, 204355, 178871, 220529]

start_date, end_date = get_start_end_dates()


update_tables = dict(despesas=True, deputados=True)

t0 = time.time()
pipeline_data_collection(update_tables, id_deputados_to_fetch, start_date, end_date)
t1 = time.time()

print(f"# Finished data collection in {round(t1 - t0, 1)} seconds\n")


update_tables = dict(despesas=True, deputados=True)

t0 = time.time()
pipeline_data_processing(update_tables)
t1 = time.time()

print(f"# Finished data processing in {round(t1 - t0, 1)} seconds\n")


print("# Finished data pipeline.")