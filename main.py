from bing_image_downloader import downloader
from PIL import Image, ImageEnhance
from random import randint
from random import random



def bing_download(query_string):

    downloader.download(query_string, limit=100, output_dir='dataset',
                        adult_filter_off=True, force_replace=False, timeout=60)


def br_correction(img):
    # image brightness enhancer
    enhancer = ImageEnhance.Brightness(img)
    factor = round(random(),1) + round(random(),1) # gives original image
    return enhancer.enhance(factor)


def cast_size(m_key, image):
    old_size = image.size
    p_image = image
    if m_key == 0:
        p_image = p_image.crop((450, 450, 1050, 1050))
        return p_image, p_image.size
    else:
        smaller = randint(0, 1)
        smaller = int((float(smaller) / 0.3 + 1) * 100)
        p_image = image.resize((old_size[0] - smaller, old_size[1] - smaller))
        max_h_offset = p_image.size[0] - 600
        max_v_offset = p_image.size[1] - 600
        left_off = randint(0, max_h_offset)
        bottom_off = randint(0, max_v_offset)
        right_off = left_off + 600
        upper_off = bottom_off + 600
        p_image = p_image.crop((left_off, bottom_off, right_off, upper_off))
        return p_image, p_image.size



def paste_on_image(w, h, img, base_img, i):
    import sys
    # print(base_img.size, "base image size")
    saved_image = base_img
    saved_over_img = img
    for j in range(0, 10):
        merged = Image.new("RGBA", base_img.size)
        if j == 0:
            saved_image = base_img
        img = saved_over_img
        random_key = randint(0, 20) % 20
        work_img, p_size = cast_size(random_key, img)
        # print(p_size, "size", img.size, "old size")

        work_base = saved_image
        work_img = br_correction(work_img)

        try:
            # work_base.paste(work_img, (x1, y1, x1 + w, y1 + h))
            merged.paste(work_base, (0, 0))
            merged.paste(work_img, (0, 0), work_img)
            # work_base = Image.alpha_composite(work_base, work_img)
        except ValueError as e:
            print(e, work_img.size, work_base.size, i, j)
            sys.exit()
        merged.save("processed/train_" + str(i) + "_" + str(j) + ".png", 'png', icc_profile=work_base.info.get('icc_profile'))


def main():
    import glob
    import sys

    image = Image.open("assets/Apple-logo.png")
    w = image.size[0]
    h = image.size[1]
    ratio = w / h

    counter = 0
    for dir in glob.glob("Dataset/*"):
        for file in glob.glob(dir+"/"+"*.*"):
            # get side closer to 200
            offset = int(abs(h - w) / 2)
            new_image = Image.open(file)
            n_h = new_image.size[1]
            n_w = new_image.size[0]
            if n_h == 1500 and n_w == 1500:
                new_image = new_image.resize((600, 600))
                paste_on_image(n_w, n_h, image, new_image, counter)
            else:
                if abs(n_w - w) < abs(n_h - h):
                    new_image = new_image.resize((w, int(w*ratio)))
                    new_image = new_image.crop([0, offset, w, h - offset])
                    new_image = new_image.resize((600, 600))
                    paste_on_image(n_w, n_h, image, new_image, counter)
                else:
                    new_image = new_image.resize((int(h*ratio), h))
                    new_image = new_image.crop([offset, 0, w - offset, h])
                    new_image = new_image.resize((600, 600))
                    paste_on_image(n_w, n_h, image, new_image, counter)

            counter+=1
            #new_image.save("processed/img_" + str(counter) + ".png")



    sys.exit()


if __name__ == "__main__":
    bing_download("books covers")
    main()
