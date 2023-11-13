from lib import BagCode


if __name__ == "__main__":
    while 1:
        try:
            code = BagCode()
            code.scan_qr_image()
            # code.alphanumeric_code = "trial_K; location_Carthage; plot_503; time_6; FieldID_4583; labID_4583"#"trial_planting_dates; variety_4533XF; date_late; pop_low; plot_603; time_6; FieldID_561; labID_561"
            code_file = code.generate_reduced_qr()
            code.print_qr_sticker(code_file)

            # "trial_K; location_Carthage; plot_503; time_6; FieldID_4583; labID_4583"
        except:
            print("Error, try again")