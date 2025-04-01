from device import Device


class TestDevice(Device):

    def __init__(self, programmer):
        super().__init__(programmer)
        print(programmer)

    def flash_size(self):
        return 350

    def write_data(self, address, data):
        print(f'==[Addr: {address} Data: {data}')

    def read_data(self, address, length):
        print(f'==[Addr: {address} Len: {length}')
        return b'ok\nits works!'[:length]

    def erase(self):
        print('==[Erase')

    def close(self):
        print('==[Close')