import os
import sys
from lib_unix import BagCode, create_csv_in_folder


if __name__ == "__main__":
    # cwd = os.getcwd() Windows only
    cwd = os.path.dirname(sys.executable)
    directory_path = os.path.join(cwd, "QRCodesReadings")
    file_path = create_csv_in_folder(directory_path)
    while 1:
        try:
            code = BagCode()
            code.scan_qr_image()
            # code.alphanumeric_code = "trial_planting_dates; variety_4533XF; date_late; pop_low; plot_603; time_6; FieldID_561; labID_561"
            code_file = code.generate_reduced_qr()
            code.print_qr_sticker(code_file)
            code.write_to_csv(file_path)
        except:
            print("Error, try again")