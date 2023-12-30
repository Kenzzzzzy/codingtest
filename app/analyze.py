import requests
from datetime import datetime
import time
import config


def analyze_image(path):
    form_data = {
        'image_path': path
    }
    
    request_time = datetime.now() 
    
    # 指定リトライ数だけループ
    for i in range(config.max_retries):
        try:
            response = requests.post(config.API_URL, data=form_data, timeout=config.api_timeout)
            
            # コールエラーを確認
            response.raise_for_status()
            
            response_time = datetime.now()
    
            # レスポンスに時刻追加
            response_json = response.json()
            response_json['resquest_time'] = request_time.isoformat()
            response_json['response_time'] = response_time.isoformat()
            
            return response_json
            
        except requests.Timeout:
            print(f'リトライ中：{i}回')
            # タイムアウトなので少し間を開ける
            time.sleep(5)
        except requests.HTTPError as http_err:
            print(f'APIエラー；{http_err}')
            break
        except Exception as e:
            print(f'予期しないエラー；{e}')
            break
