from thermal_usb import send_bytes

def print_text(msg: str):
    esc_init = b"\x1b@"  
    text_bytes = msg.encode("ascii", "ignore") + b"\n\n"
    send_bytes(esc_init + text_bytes)

if __name__ == "__main__":
    import sys
    print_text(sys.argv[1])
