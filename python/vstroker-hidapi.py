import sys
import hid
import time

class VStrokerDevice(object):
    VID = 0x0451
    PID = 0x55a5
    PRODUCT_NAME = "Vstroker"

    def __init__(self):
        self._device = None

    @staticmethod
    def getDeviceList():
        devices = []
        for d in hid.enumerate(VStrokerDevice.VID, VStrokerDevice.PID):
            # The device actually uses TI's VID, meaning the 55a5 PID is
            # probably for their CC2500 dongle. Therefore, make sure we have
            # check the product string is set, so we don't just access any ol'
            # CC2500 dongle. Once I actually /have/ a CC2500 dongle this may
            # change.
            if d["product_string"] != "Vstroker":
                continue
            devices.append(d["path"])
        return devices

    def open(self, path):
        self._device = hid.device()
        self._device.open_path(path)

    def readLoop(self):
        self._device.set_nonblocking(1)

        while True:
            data = self._device.read(10)
            if len(data) == 0:
                yield None
                continue
            axis = []
            xor_byte = data[0]
            for i in range(3):
                a = (((data[(i*2)+1] & 0xf) << 4) | (data[(i*2)+1] >> 4)) ^ xor_byte
                b = (((data[(i*2)+2] & 0xf) << 4) | (data[(i*2)+2] >> 4)) ^ xor_byte
                c = a | (b << 8)
                # convert to signed 16-bit int
                if c > 2**15:
                    c = c - 2**16
                axis.append(c)
            yield axis

def main():
    d = VStrokerDevice.getDeviceList()
    if len(d) == 0:
        print "No devices found!"
        return 1
    v = VStrokerDevice()
    v.open(d[0])
    g = v.readLoop()
    try:
        c = 0
        s = time.time()
        while True:
            l = g.next()            
            if l is None:
                time.sleep(.004)
                continue
            c = c + 1
            e = time.time()
            if e - s > 1.0:
                print c
                c = 0
                s = time.time()
    except KeyboardInterrupt:
        return 0

if __name__ == "__main__":
    sys.exit(main())
