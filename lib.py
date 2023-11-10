import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from tempfile import SpooledTemporaryFile, NamedTemporaryFile
from PIL import Image, ImageWin, ImageDraw, ImageFont
from textwrap import wrap
import win32print
import win32ui
import win32con


IMG_PATH = ".\\mizzouLogo.png"
class BagCode:
    def scan_qr_image(self):
        self.alphanumeric_code = input()

    def print_qr_sticker(self, file):
        image = Image.open(file)

        printer_name = win32print.GetDefaultPrinter()
        pdc = win32ui.CreateDC()
        pdc.CreatePrinterDC(printer_name)
        printable_width = pdc.GetDeviceCaps(win32con.HORZRES)
        printable_height = pdc.GetDeviceCaps(win32con.VERTRES)

        image_aspect = image.width / image.height
        new_width = printable_width
        new_height = int(printable_width / image_aspect)

        if new_height > printable_height:
            new_height = printable_height
            new_width = int(printable_height * image_aspect)

        image = image.resize((new_width, new_height), Image.LANCZOS)
        x_pos = (printable_width - new_width) // 2
        y_pos = (printable_height - new_height) // 2

        pdc.StartDoc(file.name)
        pdc.StartPage()
        dib = ImageWin.Dib(image)
        dib.draw(pdc.GetHandleOutput(), (x_pos, y_pos, printable_width, printable_height))
        pdc.EndPage()
        pdc.EndDoc()
        pdc.DeleteDC()

    def generate_reduced_qr(self) -> SpooledTemporaryFile:
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
        qr.add_data(self.alphanumeric_code)
        qr.make(fit=True)
        img = qr.make_image(image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer(), embeded_image_path=IMG_PATH)
        draw = ImageDraw.Draw(img)
        text_group_name = "Soybean Farming Systems"
        text_trial_year = "2023"
        font = ImageFont.truetype(
                ".\\GraphikLight.otf", 20)
        draw.text((0, 0), text="\n".join(wrap(text_group_name, width=40)), fill=(0, 0, 0), font=font)
        draw.text((img.pixel_size, 0), text="\n".join(wrap(text_trial_year, width=40)), fill=(0, 0, 0), font=font, anchor="ra")

        temp_file = NamedTemporaryFile(delete=True, suffix=".png")
        img.save(temp_file, "PNG")
        temp_file.seek(0)
        return temp_file