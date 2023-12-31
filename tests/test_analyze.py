import pytest
from unittest.mock import MagicMock
from app.analyze import analyze_image
import config
import requests

def test_analyze_image_success(mocker):
    # Analyze内で呼ばれるAPIのモック生成
    mock_post = mocker.patch('requests.post')
    
    # APIの想定戻り値
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'success': True,
        'message': 'success',
        'estimated_data': {
            'class': 3,
            'confidence': 0.8683
        }
    }
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response
    
    # テスト実行
    response = analyze_image('images/test.jpg')
    assert response['success'] == True
    assert 'resquest_time' in response  
    assert 'response_time' in response  

    mock_post.assert_called_once_with(config.API_URL, data={'image_path': 'images/test.jpg'}, timeout=config.api_timeout)
    
    
def test_analyze_image_error(mocker):
    # Analyze内で呼ばれるAPIのモック生成
    mock_post = mocker.patch('requests.post')
    
    # APIの想定戻り値
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'success': False,
        'message': 'Error:E50012',
        'estimated_data': {
        }
    }
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response
    
    # テスト実行
    response = analyze_image('images/test2.jpg')
    assert response['success'] == False
    mock_post.assert_called_once_with(config.API_URL, data={'image_path': 'images/test2.jpg'}, timeout=config.api_timeout)


def test_analyze_image_timeout(mocker):
    # タイムアウトするよう指定
    mocker.patch('requests.post', side_effect=requests.Timeout)

    # 例外が発生することを確認
    with pytest.raises(requests.Timeout):
        analyze_image("images/test.jpg")        


def test_analyze_image_500error(mocker):
    mock_post = mocker.patch('requests.post')
    
    # ステータスコード設定
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.raise_for_status.side_effect = requests.HTTPError(response=mock_response)
    
    mocker.patch('requests.post', return_value=mock_response)
    
    with pytest.raises(requests.HTTPError):
        analyze_image("images/test.jpg")
    