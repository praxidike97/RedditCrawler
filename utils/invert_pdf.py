# Code taken from https://github.com/Lyonk71/invert-pdf-color/blob/master/invert_pdf_color/invert.py

#from pdf2image import convert_from_path

#from PIL import ImageOps
#import img2pdf
import os


def invert_color(filepath):

    print("Vor convert")
    os.mkdir("tmp")
    images = convert_from_path(filepath, output_folder="tmp")

    print("Vor enumerate")
    idx_counter = []
    for idx, i in enumerate(images):
        idx_counter.append('output' + str(idx) + ".jpeg")
        i = ImageOps.invert(i)
        i.save('output' + str(idx) + '.jpeg')

    print("Vor write")
    filename = filepath.split("/")[-1].split(".")[0]
    with open("./pdf_output/%s_dark-mode.pdf"%filename, "wb") as f:
        f.write(img2pdf.convert(idx_counter))
    print("Nach write")

    for i in idx_counter:
        os.remove(i)