from programmer import Programmer


class TestProgrammer(Programmer):

    def set_vcc(self, voltage):
        print(f'==[Set VCC: {voltage}')

    def set_vpp(self, voltage):
        print(f'==[Set VPP: {voltage}')

    def set_param(self, param, value):
        print(f'==[Set param: {param}={value}')

    def send_data(self, protocol, data):
        print(f'==[Send data Protocol: {protocol} Data: {data}')

    def receive_data(self, protocol):
        print(f'==[Receive data Protocol: {protocol}')

    def exit(self):
        print('==[Exit')