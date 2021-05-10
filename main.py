from PIL import Image, ImageDraw
from fpdf import FPDF



IMAGE_FOLDER = "images/"
IMAGE_1 = IMAGE_FOLDER + "test3.png"
IMAGE_2 = IMAGE_FOLDER + "test1.png"

FACTOR = 1000
COLS = 100
ROWS = 100


def region_analyze(image, x, y, width, height, factor=FACTOR):
    region_status = 0
    for x_cord in range(x, x + width):
        for y_cord in range(y, y + height):
            try:
                pixel = image.getpixel((x_cord, y_cord))
                region_status += int(sum(pixel) / 3)
            except:
                return None
    return region_status // factor


def analyze(image_ref, image_target, col=COLS, row=ROWS):
    reference = Image.open(image_ref)
    target = Image.open(image_target)

    width, height = reference.size
    block_width = width // col
    block_height = height // row

    has_diff = False

    for x in range(0, width, block_width + 1):
        for y in range(0, height, block_height + 1):
            region_ref = region_analyze(reference, x, y, block_width, block_height)
            region_target = region_analyze(target, x, y, block_width, block_height)

            if region_ref and region_target and region_ref != region_target:
                has_diff = True
                draw = ImageDraw.Draw(reference)
                draw.rectangle((x - 1, y - 1, x + block_width, y + block_height), outline="red")


    if has_diff:
        reference.save("diff.png")


    else:
       print("Изображения идентичны: FACTOR {f}, COLS {c}, ROWS {r}".format(f=FACTOR, c=COLS, r=ROWS))


class PDF(FPDF):
    def header(self):
        # Logo
        self.image('images/test1.png', 5, 8, 100)
        self.image('diff.png', 110, 8, 100)

# Create a PDF object
pdf = PDF('P', 'mm', 'Letter')

# get total page numbers
pdf.alias_nb_pages()

# Set auto page break
pdf.set_auto_page_break(auto=True, margin=15)

# Add Page
pdf.add_page()

# specify font
pdf.add_font('DejaVu', '', 'DejaVuSans-ExtraLight.ttf', uni=True)
pdf.set_font('DejaVu', '', 14)
pdf.cell(5, 160, txt="Исходное изображение", ln=0, align="L")
pdf.cell(180, 160, txt="Полученное изображение", ln=0, align="R")

pdf.output('pdf_report.pdf')




analyze(IMAGE_1, IMAGE_2)
