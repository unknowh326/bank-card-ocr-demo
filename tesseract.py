import cv2
import pytesseract
from PIL import Image

# ========== Tesseract 配置（Windows需要修改为自己本地tesseract.exe路径） ==========
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# 测试图片路径，使用时自行修改
IMAGE_PATH = "D:\\pythonworkplace\\pythonProject8\\yhk.png"


def format_num(num: str) -> str:
    """卡号格式化，每4个数字加空格"""
    return ' '.join([num[i:i+4] for i in range(0, len(num), 4)])


def recognize_bank_card(image_path: str):
    # 1. 读取图片
    img = cv2.imread(image_path)
    if img is None:
        print("图片读取失败！检查路径")
        return None

    # 2. 图像预处理：灰度 + 高斯降噪 + Otsu二值化（适配银行卡反光、噪声）
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    _, binary = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 3. Tesseract配置：只识别数字
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'
    card_num = pytesseract.image_to_string(binary, config=custom_config).strip()

    # 4. 过滤掉识别出来的非数字字符
    card_num = ''.join([c for c in card_num if c.isdigit()])

    # 5. 格式化卡号输出
    formatted_num = format_num(card_num)
    print(f"识别卡号: {card_num}")
    print(f"格式化卡号: {formatted_num}")

    # 6. 在图片上标注识别结果
    h, w = img.shape[:2]
    cv2.putText(img, f"OCR: {card_num}", (20, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
    cv2.putText(img, f"Card: {formatted_num}", (20, h - 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

    # 7. 保存、展示结果图
    cv2.imwrite("bank_card_result.png", img)
    cv2.imshow("Bank Card OCR Result", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return card_num


if __name__ == "__main__":
    recognize_bank_card(IMAGE_PATH)
