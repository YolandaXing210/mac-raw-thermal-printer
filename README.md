# Mac Raw USB Thermal Printer (ESC/POS + Python)

This project shows how to print **images and text** directly to a cheap 58mm thermal printer from macOS using **raw USB control**, **Python**, and **ESC/POS commands** — completely bypassing CUPS, drivers, and printer restrictions.

It works with printers that use the common chipset:
- **Vendor ID:** `0x28e9`
- **Product ID:** `0x0289`
- or any ESC/POS-compatible 58mm mini printer

This guide includes:
✔ Full setup for macOS  
✔ USB endpoint detection  
✔ ESC/POS raw command sending  
✔ Image printing (PNG → thermal poster)  
✔ Text printing  
✔ Complete working scripts  

This entire workflow was reverse-engineered from scratch, tested, and verified on macOS Sonoma.

---

## ✦ Features

- Print PNG/JPG images from Mac  
- Print ASCII text  
- Works over **USB**, not Bluetooth  
- No drivers, no CUPS, no PostScript  
- Pure Python → Raw ESC/POS bytes  
- Supports any ESC/POS thermal printer with USB endpoints

This project is ideal for:
- creative coding  
- zine printing  
- tiny posters  
- generative art  
- interactive installations  
- ticket-style UX experiments  

---

# 1. Install Requirements

```bash
brew install libusb
python3 -m pip install --user pyusb
python3 -m pip install --user Pillow
```
# 2. Device Setup

Plug in your thermal printer → then detect it with Python.

### 2.1 List all USB devices

```bash
python3 - << 'EOF'
import usb.core
for dev in usb.core.find(find_all=True):
    print(hex(dev.idVendor), hex(dev.idProduct))
EOF
```

You should see something like:

```
0x28e9 0x0289   ← your thermal printer
```

### 2.2 Inspect the printer's endpoints
```
python3 - << 'EOF'
import usb.core, usb.util

dev = usb.core.find(idVendor=0x28e9, idProduct=0x0289)
if dev is None:
    print("Printer not found")
else:
    print("Found device")
    for cfg in dev:
        print("Config:", cfg.bConfigurationValue)
        for intf in cfg:
            print(" Interface:", intf.bInterfaceNumber)
            for ep in intf:
                print("  Endpoint:", hex(ep.bEndpointAddress))
EOF
```
Typical output:
```
Found device
Config: 1
 Interface: 0
  Endpoint: 0x1   ← OUT endpoint (write here)
  Endpoint: 0x81  ← IN endpoint (rarely used)
```
This confirms macOS is seeing the printer at a USB level.

# 3. Image Guidelines
For the best thermal poster results:
- Max width: 384px
- Color: use black & white or very high contrast
- Avoid gradients (thermal can’t render grayscale well)
- Bold shapes print best
- Dithered images look artistic
- White = no heat = no ink
- Black = heat = printed dots
- 0 Alpha = no heat = no ink
- Thin lines may break during thresholding
Recommended style:
- graphic silhouettes
- pixel designs
- linework
- bold typography
- mini-zine aesthetics


# 4. Known Good Printers
This method fully works with:
- PT-210
- Any 58mm printer with vendor ID 28e9
- Any ESC/POS-compatible device with USB OUT endpoint

