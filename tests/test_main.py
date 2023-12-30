import pytest
from unittest.mock import MagicMock
import main


def test_main_success(mocker):
    """
    画像分析のAPIのみモック化して全体のテスト（成功パターン）
    """
    
    # 成功する画像
    mocker.patch('sys.argv', ['main.py', 'images/test.jpg'])

    # Analyze内で呼ばれるAPIのモック生成
    mock_post = mocker.patch('requests.post')
    
    # Success想定の戻り値
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
    
    main.main()


def test_main_fail(mocker):
    """
    画像分析のAPIのみモック化して全体のテスト（失敗パターン）
    """
    
    # 成功する画像
    mocker.patch('sys.argv', ['main.py', 'images/test2.jpg'])

    # Analyze内で呼ばれるAPIのモック生成
    mock_post = mocker.patch('requests.post')
    
    # Success想定の戻り値
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'success': False,
        'message': 'Error:E50012',
        'estimated_data': {
        }
    }
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response    
    
    main.main()


def test_main_not_exists(mocker):
    """
    画像分析のAPIのみモック化して全体のテスト（画像無しパターン）
    """
    
    # 存在しない画像
    mocker.patch('sys.argv', ['main.py', 'images/test3.jpg'])    
    main.main()
    

def test_main_not_params(mocker):
    """
    画像分析のAPIのみモック化して全体のテスト（画像指定無しパターン）
    """
    
    # 存在しない画像
    mocker.patch('sys.argv', ['main.py'])    
    main.main()
