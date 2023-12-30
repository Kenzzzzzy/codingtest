import requests
from datetime import datetime
import time
import config


def analyze_image(path):
    """
    画像分析APIをコールする
    
    Paramaters
    ---
    path : str
        画像パス
    """
    
    form_data = {
        'image_path': path
    }
    
    
    # 指定リトライ数だけループ
    for i in range(config.max_retries):
        try:
            request_time = datetime.now().timestamp()

            response = requests.post(config.API_URL, data=form_data, timeout=config.api_timeout)
            
            response_time = datetime.now().timestamp()

            # コールエラーを確認
            response.raise_for_status()
            
            # レスポンス整形
            temp = response.json()
            response_json = {
                'image_path': path,
                'success': temp['success'],
                'message': temp['message'],
                'class': temp['estimated_data'].get('class', None),
                'confidence': temp['estimated_data'].get('confidence', None),
                'request_timestamp': int(request_time),
                'response_timestamp': int(response_time)
            } 

            print(f'レスポンス：{response_json}')
            return response_json
            
        except requests.Timeout:
            if i == config.max_retries - 1:
                print('タイムアウト')
                raise
            else:
                # タイムアウトなので少し間を開ける
                time.sleep(1)
                print(f'リトライ：{i+1}回')
        except requests.HTTPError as http_err:
            print(f'APIエラー：{http_err.response.status_code}')
            raise
        except Exception as e:
            print(f'予期しないエラー；{e}')
            raise
