


def pipeline_data_collection(update_tables, id_deputados_to_fetch=[],
                             start_date=None, end_date=None):
    from src.collectors import collect_data_from_api, collect_despesas_from_api
    from src.utils import get_month_list_in_interval

    if update_tables['deputados']:
        collect_data_from_api('raw', 'deputados')
        
    if update_tables['despesas']:
        interval_to_fetch = get_month_list_in_interval(start_date, end_date)
        for id_deputado in id_deputados_to_fetch:
            for dt in interval_to_fetch:
                collect_despesas_from_api(id_deputado, ano=dt.year, mes=dt.month)




def pipeline_data_processing(update_tables):
    from src.preprocessing import process_deputados, process_despesas, process_gold_table
    if update_tables['deputados']:
        process_deputados()
    if update_tables['despesas']:
        process_despesas()

    process_gold_table()


