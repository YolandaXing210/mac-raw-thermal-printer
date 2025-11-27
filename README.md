# mac-raw-thermal-printer
mac-raw-thermal-printer
🧊 Mac → USB → ESC/POS Thermal Printing
Printing images + text directly to a 58mm thermal printer on macOS (no drivers, no CUPS)
This repo shows how to print clean text + images to a cheap 58mm thermal receipt printer directly over USB on macOS.
No drivers.
No CUPS.
No PostScript garbage.
Just raw ESC/POS bytes.
I wanted full control. So I bypassed macOS’s printing pipeline entirely and talked to the printer’s USB endpoint myself. Turns out — it works great.
✨ What This Solves
macOS always tries to convert print jobs into PDF → PostScript.
Thermal printers don’t speak PostScript.
So you get endless trash like:
%!PS-Adobe-3.0
%%Creator: cgpdftops
...
This repo avoids that completely.
🧩 How It Works
macOS sees the printer as a USB device (VID/PID)
Python + pyusb lets us open the USB OUT endpoint
We send raw ESC/POS commands directly
Printer prints exactly what we tell it
This is the same low-level approach used by embedded systems.
📦 Install (macOS)
brew install libusb
python3 -m pip install --user pyusb Pillow
📁 Folder Setup
thermal-printer/
    thermal_usb.py
    print_text.py
    print_image.py
