import glob
from os import path
import os
from aip import AipOcr
from PIL import Image

def convertimg(picfile, outdir):

    img = Image.open(picfile)
    width, height = img.size
    while (width * height > 4000000):  # 该数值压缩后的图片大约 两百多k
        width = width // 2
        height = height // 2
    new_img = img.resize((width, height), Image.BILINEAR)
    new_img.save(path.join(outdir, os.path.basename(picfile)))


def prepareWork():
    os.chdir("D:/python编程/SWork/Include/pictures")
    os.getenv('ENV_PORT')
    os.environ.get('ENV_PORT')

def myOCR(picfile):
    prepareWork()
    filename = path.basename(picfile)
    print("正在识别图片：\t" + filename)
    s="tesseract D:\\python编程\\SWork\\Include\\"\
      +picfile+" "+filename.strip(".png").strip(".jpg")+" -l chi_sim"
    os.system(s)
    with open(filename.strip(".png").strip(".jpg")+
              ".txt", 'rb') as f:
        s2 = f.read()
    os.system("del *.txt")
    f2 = open('../text.txt','ab+')
    f2.write(s2)
    f2.close()
    print("识别成功！")
    print("文本导出成功！")
    print()


if __name__ == "__main__":
    outfile = 'text.txt'
    outdir = 'tmp'
    if path.exists(outfile):
        os.remove(outfile)
    if not path.exists(outdir):
        os.mkdir(outdir)
    print("压缩过大的图片...")
    # 首先对过大的图片进行压缩，以提高识别速度，将压缩的图片保存与临时文件夹中
    for picfile in glob.glob("pictures/*"):
        convertimg(picfile, outdir)
    print("图片识别...")
    for picfile in glob.glob("tmp/*"):
        myOCR(picfile)
        os.chdir("D:\\python编程\\SWork\\Include")
        os.remove(picfile)
    print('图片文本提取结束！文本输出结果位于 %s 文件中。' % outfile)
    os.removedirs(outdir)
