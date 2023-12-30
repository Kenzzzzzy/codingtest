import sys
import os
from app.analyze import analyze_image
from app.database import save_analysis_result

def main():
    if len(sys.argv) == 1:
        print('画像ファイルのパスを指定してください')
        return
    
    image_path = sys.argv[1]
    
    if not os.path.exists(image_path):
        print('画像ファイルが見つかりません')
        return
    
    image_info = analyze_image(image_path)

    if image_info is None:
        print('失敗')
    else:
        save_analysis_result(image_info)


if __name__ == "__main__":
    main()
    