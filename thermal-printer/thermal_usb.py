# thermal_usb.py
import usb.core
import usb.util

VENDOR_ID = 0x28e9
PRODUCT_ID = 0x0289

def get_printer():
    dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
    if dev is None:
        raise RuntimeError("Printer not found. Is it plugged in and on?")

    # Detach kernel driver if needed (sometimes not required on macOS)
    try:
        if dev.is_kernel_driver_active(0):
            dev.detach_kernel_driver(0)
    except Exception:
        pass

    dev.set_configuration()
    cfg = dev.get_active_configuration()
    intf = cfg[(0, 0)]

    out_ep = None
    for ep in intf:
        if usb.util.endpoint_direction(ep.bEndpointAddress) == usb.util.ENDPOINT_OUT:
            out_ep = ep
            break

    if out_ep is None:
        raise RuntimeError("Could not find OUT endpoint")

    return dev, out_ep

def send_bytes(data: bytes):
    _, out_ep = get_printer()
    out_ep.write(data)
