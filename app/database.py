import os
import pymysql

def get_db_connection():
    """
    環境変数から接続情報を取得
    """
    return pymysql.connect(
        host = os.environ.get('DB_HOST'),
        user = os.environ.get('DB_USER'),
        password = os.environ.get('DB_PASSWORD'),
        db = os.environ.get('DB_NAME'),
        charset = 'utf8mb4',
    )
    

def save_analysis_result(data):
    """
    DBに画像分析結果を保存する
    
    Paramaters
    -----
    """
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = """
            INSERT INTO ai_analysis_log (image_path, success, message, class, confidence, request_timestamp, response_timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                data['image_path'],
                data['success'],
                data['message'],
                data['class'],
                data['confidence'],
                data['request_timestamp'],
                data['response_timestamp']
            ))
            
        connection.commit()
    except pymysql.MySQLError as e:
        print(f"DBエラー：{e}")
        if connection:
            connection.rollback()
        raise
    finally:
        if connection:
            connection.close()