from Register import Register
from PIL import Image

im1 = Image.open("0001.jpg")
im2 = Image.open("0068.jpg")
im1.convert('L').save('pyimreg-master/temp/1.pgm')
im2.convert('L').save('pyimreg-master/temp/2.pgm')
#im1 = asarray(im1)
#im2 = asarray(im2)

reg = Register
reg(im1,im2)
