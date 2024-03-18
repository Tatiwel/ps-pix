import cv2
import matplotlib.pyplot as plt
import qrcode

# carregar imagem
img = cv2.imread("qrcode_tester.png")

# achar qr code
detector = cv2.QRCodeDetector()
data, bbox, straight_qrcode = detector.detectAndDecode(img)
print(data)

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=0,
)
qr.add_data(data)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save("qrcode.bmp")
plt.imshow(img)
plt.show()
