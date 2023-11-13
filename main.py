from lib import BagCode


if __name__ == "__main__":
    while 1:
        code = BagCode()
        code.scan_qr_image()
        # code.alphanumeric_code = "trial_K; location_Carthage; plot_503; time_6; FieldID_4583; labID_4583"
        code_file = code.generate_reduced_qr()
        code.print_qr_sticker(code_file)