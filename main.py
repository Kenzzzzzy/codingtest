import sys
import os
from app.analyze import analyze_image


def main():
    if len(sys.argv) == 1:
        print('画像ファイルのパスを指定してください')
        exit()
    
    image_path = sys.argv[1]
    
    if not os.path.exists(image_path):
        print('画像ファイルが見つかりません')
        exit()
    
    analyze_image(image_path)


if __name__ == "__main__":
    main()
    