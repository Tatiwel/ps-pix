from PIL import Image

file_in = "qrcode_test.jpg"
img = Image.open(file_in)

size = 64, 64

img.thumbnail(size, Image.Resampling.NEAREST)

img = img.convert("1")

file_out = "qrcode_test.bmp"
img.save(file_out)
