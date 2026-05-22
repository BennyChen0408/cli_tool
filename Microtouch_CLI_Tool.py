import hid
import argparse

VID = 0x0596
PID = 0x05ED
TARGET_PATH = b'\\\\?\\HID#VID_0596&PID_05ED&Col03#6&e1f519a&17&0002#{4d1e55b2-f16f-11cf-88cb-001111000030}'

REPORT_FW     = 0x17
REPORT_MATRIX = 0x20

def open_device():
    device = hid.device()
    device.open_path(TARGET_PATH)
    return device

def get_firmware_version():
    device = open_device()
    try:
        print(f"Manufacturer : {device.get_manufacturer_string()}")
        print(f"Product      : {device.get_product_string()}")
        print("-" * 40)

        response = device.get_feature_report(REPORT_FW, 4)

        if len(response) >= 3:
            major = response[1]
            minor = response[2]
            print(f"Raw Response     : {[f'{b:02X}' for b in response]}")
            print(f"Firmware Version : {major}.{minor:02X}")
        else:
            print("Response too short")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        device.close()

def get_matrix_size():
    device = open_device()
    try:
        print(f"Manufacturer : {device.get_manufacturer_string()}")
        print(f"Product      : {device.get_product_string()}")
        print("-" * 40)

        response = device.get_feature_report(REPORT_MATRIX, 4)

        if len(response) >= 3:
            x_size = response[1]
            y_size = response[2]
            print(f"Raw Response : {[f'{b:02X}' for b in response]}")
            print(f"Matrix Size  : X={x_size}, Y={y_size}")
        else:
            print("Response too short")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        device.close()

def main():
    parser = argparse.ArgumentParser(description="3M MicroTouch HID Tool")
    parser.add_argument("-f", action="store_true", help="Show Firmware version")
    parser.add_argument("-m", action="store_true", help="Show Matrix Size")
    args = parser.parse_args()

    if args.f:
        get_firmware_version()
    elif args.m:
        get_matrix_size()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()