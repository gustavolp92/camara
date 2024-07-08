from dotenv import load_dotenv
import os
import glob
import yaml


def _read_yaml(path: str):
    """
    Reads yaml file in path passed as parameter.
    """
    return yaml.load(open(path), Loader=yaml.FullLoader)



def get_config(dot_env_path=None):
    """
    Returns:
        dict with config info.
    Store configuration files in dict object.
    Path of folder with files should be added as an environment variable named 'PROJECT_CONFIG_PATH', in a '.env' file (reference: https://pypi.org/project/python-dotenv/).
    The config folder can have multiple config files (i.e., 01-connections.yaml, 02-data.yaml, 03-model.yaml, etc.). All will be added to a single config object.
    Each 'cleaned' file name (i.e., connections, data, model) will be a dict key to the content inside the file.
    
    NOTE: when running code from workspace (or anywhere outside of repo environment), it may be necessary to first create an environment variable with the path to config files. it may be done with the following code:
            import os
            os.environ['PROJECT_CONFIG_PATH'] = <here_goes_path_to_config_files>
    """
    def _clean_config_file_name(name):
        tmp = name.split('\\')[-1]
        tmp = tmp.split('-')[-1]
        tmp = tmp.split('.')[0]
        return tmp
    
    # load_dotenv(dot_env_path)  #get environment variables from '.env' file
    # config_path = f"{os.environ['PROJECT_CONFIG_PATH']}"
    import os
    current_dir = os.path.dirname(os.path.realpath(__name__))
    config_path = os.path.abspath(os.path.join(current_dir, 'config'))
    print(config_path)
    file_paths = glob.glob(f"{config_path}/*")
    config = dict()
    files = []
    for file_path in file_paths:
        high_level_key = _clean_config_file_name(file_path)
        config[high_level_key] = _read_yaml(file_path)
    return config


def read_json(domain, source_name):
    import json
    from src.io import get_config
    
    config = get_config('src/.env')['data']
    source = config[domain][source_name]
    file_path = f"{source['destination_path']}/{source_name}.{source['format']}"
     
    # Abra o arquivo no modo de leitura e use json.load() para carregar os dados do arquivo
    with open(file_path, "r") as json_file:
        data = json.load(json_file)
    return data



def save_json(data, file_path):
    import json
    from src.utils import ensure_folder_exists

    folder_path = file_path.rsplit('\\', 1)[0]
    ensure_folder_exists(folder_path)

    with open(file_path, "w") as json_file:
        json.dump(data, json_file)