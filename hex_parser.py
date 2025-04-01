class HexParser:
    address = None
    data = None
    rtype = None

    def parse_record(self, record):
        size = int(record[:2], 16)
        addr = int(record[2:6], 16)
        rtype = int(record[6:8], 16)
        data = []
        for i in range(size + 1):
            off = i * 2 + 8
            data.append(int(record[off:off + 2], 16))
        csum = data.pop()
        if ~(size + rtype + (addr & 0xFF) + (addr >> 8 & 0xFF) + sum(data)) - csum + 1 & 0xFF:
            raise Exception('Checksum error')
        self.data = None
        self.rtype = rtype
        match rtype:
            case 0x00:
                self.data = data
                self.address = addr
            case _:
                self.address = None