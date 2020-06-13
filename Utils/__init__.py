import json
from collections import OrderedDict


def create_config():
    try:
        file_data = OrderedDict()
        file_data['Token'] = '<Disocrd Token>'
        file_data['command_prefix'] = '!'
        file_data['description'] = 'New experience\nmore experience'
        file_data['Auther'] = 'zeroday0619#0619'
        file_data['mongodb_url'] = '<mongo db url>'
        file_data['mongodb_port'] = '<mongo db port>'
        file_data['X-Naver-Client-Id'] = '<NAVER OPEN API - Client ID>'
        file_data['X-Naver-Client-Secret'] = '<NAVER OPEN API - Client Secret>'
        with open('config.json', 'w', encoding='utf-8') as CreateConfig:
            json.dump(file_data, CreateConfig, ensure_ascii=False, indent='\t')
    except Exception as ex:
        print("[X]: ERROR\n")
        print(f"{str(ex)}")
        exit()


with open('config.json', 'r', encoding='utf-8') as _config:
    config = json.load(_config)
