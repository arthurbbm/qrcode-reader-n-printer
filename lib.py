import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from tempfile import SpooledTemporaryFile, NamedTemporaryFile
from PIL import Image, ImageWin, ImageDraw, ImageFont
import win32print
import win32ui
import win32con


dict_replace = {"trial": "Trial",
                "location": "Location",
                "plot": "Plot",
                "time": "Time",
                "FieldID": "Field ID",
                "labID": "Lab ID",
                "variety": "Variety",
                "pop": "Population",
                "date": "Date",
                "planting_dates": "Planting Dates"}

IMG_PATH = "./mizzouLogo.png"
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

    def __make_background_image(self, width, height):
        image = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(image)
        outer_left, outer_top, outer_right, outer_bottom = 0, 0, width, height
        draw.rectangle([outer_left, outer_top, outer_right, outer_bottom], fill='white')
        return image

    def __make_qr_image(self, alphanumeric_code):
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=4, border=0)
        qr.add_data(alphanumeric_code)
        qr.make(fit=True)
        img = qr.make_image(image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer(),
                            embeded_image_path=IMG_PATH)
        return img

    def __convert_alphanumeric_to_dict(self, alphanumeric_code):
        code_dict = {}
        code_list = alphanumeric_code.split("; ")
        for code in code_list:
            key, value = code.split("_", 1)
            code_dict[key] = value
        return code_dict

    def __draw_dict_to_image(self, image, code, font_body_size, line_spacing, width, y_text):
        font_body = ImageFont.truetype(
            "./Arial Black.ttf", font_body_size)
        for key, value in code.items():
            key = dict_replace[key]
            value = value.upper() if value not in dict_replace else dict_replace[value]
            image.text((6, y_text), key, fill="black", font=font_body)
            image.text((width // 2 - 4, y_text), value, fill="black", font=font_body)
            y_text += font_body_size + line_spacing
        return image

    def __make_text_image(self, text, width, height):
        img = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(img)
        text_group_name = "Soybean Farming Systems"
        text_trial_year = "2023"
        font_header = ImageFont.truetype(
                "./Arial Black.ttf", 14)
        draw.text((3, 0), text=text_group_name, fill=(0, 0, 0), font=font_header)
        draw.text((3, 15), text=text_trial_year, fill=(0, 0, 0), font=font_header)

        code = self.__convert_alphanumeric_to_dict(text)

        self.__draw_dict_to_image(draw, code, 14, 2, width, 35)

        return img
    def generate_reduced_qr(self) -> SpooledTemporaryFile:
        width, height = 216, 384
        image = Image.new('RGB', (width, height), 'white')
        background_image = self.__make_background_image(width, height)
        qr_image = self.__make_qr_image(self.alphanumeric_code)
        text_image = self.__make_text_image(self.alphanumeric_code, width, int(height/2.5))

        image.paste(background_image, (0, 0))
        qr_image_offset = int((width - qr_image.pixel_size) / 2), int((height/2.5 + qr_image.pixel_size - 30) / 2)
        image.paste(qr_image, qr_image_offset)
        image.paste(text_image, (0, 0))

        temp_file = NamedTemporaryFile(delete=True, suffix=".png")
        image.save(temp_file, "PNG")
        temp_file.seek(0)
        return temp_file