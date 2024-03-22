#############################################################################################
# RoboCore - IoT Night Light - Notificacao de Presenca
# Envia uma notificacao pelo aplicativo IFTTT quando o sensor identificar uma presenca
#############################################################################################

# inclusao das bibliotecas
from machine import Pin, SoftI2C
import libs.view.ssd1306 as ssd1306
from libs.img.bmp_reader import BMPReader
from time import sleep

# criacao do objeto do barramento I2C
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

# criacao do objeto do display OLED
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# leitura do arquivo BMP
def lebytes_to_int(bytes):
    n = 0x00
    while len(bytes) > 0:
        n <<= 8
        n |= bytes.pop()
    return int(n)


with open("qrcode_test.bmp", "rb") as f:
    img_bytes = list(bytearray(f.read()))

start_pos = lebytes_to_int(img_bytes[10:14])
end_pos = start_pos + lebytes_to_int(img_bytes[34:38])

width = lebytes_to_int(img_bytes[18:22])
height = lebytes_to_int(img_bytes[22:26])

pixel_data = img_bytes[start_pos:end_pos]

oled.fill(0)
oled.drawBitmap(0, 0, bytearray(pixel_data), 64, 64)
oled.show()