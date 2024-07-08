import requests
import os

def collect_data_from_api(domain, source_name):
    from src.io import get_config, save_json

    config = get_config('src/.env')['data']
    source = config[domain][source_name]
    file_path = os.path.join(source['destination_path'], f"{source_name}.{source['format']}")

    requisicao = requests.get(source['base_link'])

    if source['format'] == 'json':
        info = requisicao.json()
        save_json(info, file_path)
    else:
        print('Unsupported format:', source['format'])
    
    print(f"Source {source_name} was saved in path: {file_path}")




def collect_despesas_from_api(id_deputado, ano, mes):
    from src.io import save_json
    from src.utils import ensure_folder_exists
    pagina = 1
    end_search = 0
    data = []
    
    while end_search == 0:
        link = f"https://dadosabertos.camara.leg.br/api/v2/deputados/{id_deputado}/despesas?ano={ano}&mes={mes}&pagina={pagina}&ordem=ASC&ordenarPor=ano"
        requisicao = requests.get(link)
        page_data = requisicao.json()['dados']
        data.extend(page_data)
        pagina = pagina + 1
        if len(page_data) == 0:
            end_search = 1

    print(f"ID:{id_deputado}, {ano}-{str(mes).zfill(2)}: {len(data)} registros")
    
    if len(data)==0:
        return
    
    folder_path = os.path.join("data","raw","despesas", str(id_deputado), str(ano))
    ensure_folder_exists(folder_path)
    file_path = os.path.join(folder_path, f"{str(mes).zfill(2)}.json")
    
    save_json(data, file_path)