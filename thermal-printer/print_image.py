# print_image.py
from PIL import Image
from thermal_usb import send_bytes

MAX_WIDTH = 384  # 58mm printer width in dots

def image_to_escpos(img: Image.Image) -> bytes:
    """
    Convert a PIL image to ESC/POS bit image.
    Uses 24-dot double-density mode (ESC * 33).
    """
    img = img.convert("1")  # 1-bit: 0 = black, 255 = white
    width, height = img.size

    if width > MAX_WIDTH:
        raise ValueError(f"Image too wide ({width}px). Max is {MAX_WIDTH}px.")

    w = width
    result = bytearray()

    # Process image in vertical stripes of 24 pixels
    for y in range(0, height, 24):
        m = 33  # 24-dot double-density
        nL = w & 0xFF
        nH = (w >> 8) & 0xFF
        # ESC * m nL nH
        result += b"\x1b*" + bytes([m, nL, nH])

        # For each column
        for x in range(w):
            # Build 3 bytes (24 vertical dots)
            for k in range(3):  # 3 * 8 = 24
                b = 0
                for bit in range(8):
                    yy = y + k * 8 + bit
                    if yy >= height:
                        continue
                    pixel = img.getpixel((x, yy))
                    if pixel == 0:  # black pixel
                        b |= 1 << (7 - bit)
                result.append(b)

        # Line feed after each stripe
        result += b"\n"

    # Extra feed at the end
    result += b"\n\n\n"
    return bytes(result)

def print_image(path: str):
    img = Image.open(path)

    # Resize to fit width while keeping aspect ratio
    w, h = img.size
    if w > MAX_WIDTH:
        new_h = int(h * (MAX_WIDTH / float(w)))
        img = img.resize((MAX_WIDTH, new_h))

    escpos_data = b"\x1b@"  # initialize printer
    escpos_data += image_to_escpos(img)

    send_bytes(escpos_data)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 print_image.py path/to/image.png")
    else:
        print_image(sys.argv[1])
