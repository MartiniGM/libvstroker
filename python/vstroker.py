import sys

class VStroker(object):
  def __init__(self):
    pass

  def readLoop(self):
    self.hidraw = open("/dev/hidraw4")
    while True:
      try:
        data = self.hidraw.read(10)
        if data == "":
          continue
        axis = []
        data = [ord(x) for x in data]
        xor_byte = data[0]
        for i in range(3):
          a = (((data[(i*2)+1] & 0xf) << 4) | (data[(i*2)+1] >> 4)) ^ xor_byte
          b = (((data[(i*2)+2] & 0xf) << 4) | (data[(i*2)+2] >> 4)) ^ xor_byte
          axis.append(a | b << 8)
        print "%s" % (axis)
      except KeyboardInterrupt:
        break

def main():
  v = VStroker()
  v.readLoop()

if __name__ == "__main__":
  sys.exit(main())