import sys
import hid

class VStrokerDevice(object):
    VID = 0x0451
    PID = 0x55a5
    PRODUCT_NAME = "Vstroker"

    def __init__(self):
        self._device = None

    def getDeviceList(self):
        for d in hid.enumerate(VStrokerDevice.VID, VStrokerDevice.PID):
            keys = d.keys()
            keys.sort()
            for key in keys:
                print "%s : %s" % (key, d[key])
            print ""

    def open(self, ):
        self._device = hid.device()
        self._device.open(0x451, 0x55a5)

    def readLoop(self):
        print "Opening device"
        h = hid.device(0x451, 0x55a5)
        #h = hid.device(0x1941, 0x8021) # Fine Offset USB Weather Station

        print "Manufacturer: %s" % h.get_manufacturer_string()
        print "Product: %s" % h.get_product_string()
        print "Serial No: %s" % h.get_serial_number_string()
        h.set_nonblocking(1)

        # self.hidraw = open("/dev/hidraw4")
        while True:
            try:
                data = h.read(10)
                if len(data) == 0:
                    continue
                axis = []
                xor_byte = data[0]
                for i in range(3):
                    a = (((data[(i*2)+1] & 0xf) << 4) | (data[(i*2)+1] >> 4)) ^ xor_byte
                    b = (((data[(i*2)+2] & 0xf) << 4) | (data[(i*2)+2] >> 4)) ^ xor_byte
                    axis.append(a | b << 8)
                print "%s" % (axis)
            except KeyboardInterrupt:
                break

def main():
    v = VStrokerDevice()
    v.getDeviceList()
    v.open()
    #v.readLoop()

if __name__ == "__main__":
    sys.exit(main())
