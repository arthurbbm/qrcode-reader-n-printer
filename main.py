from lib import BagCode


if __name__ == "__main__":
    while 1:
        code = BagCode()
        code.scan_qr_image()
        code_file = code.generate_reduced_qr()
        code.print_qr_sticker(code_file)