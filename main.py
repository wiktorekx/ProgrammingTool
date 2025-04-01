import argparse
import importlib
import os.path

import hex_parser
from device import Device
from programmer import Programmer

def load_class(module, class_name):
    return getattr(importlib.import_module(module + '.' + class_name), ''.join(map(lambda x: x.capitalize(), class_name.split('_'))))

if __name__ == '__main__':
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("--programmer", required=True)
    argument_parser.add_argument("--device", required=True)
    argument_parser.add_argument('action', choices=['erase', 'program', 'dump'])
    argument_parser.add_argument('format', choices=['bin', 'hex'], nargs='?')
    argument_parser.add_argument('file', nargs='?')
    args = argument_parser.parse_args()
    if not os.path.exists(f'programmers/{args.programmer}.py'):
        raise Exception(f'Not found programmer {args.programmer}')
    if not os.path.exists(f'devices/{args.device}.py'):
        raise Exception(f'Not found device {args.device}')
    programmer = load_class('programmers', args.programmer)()
    if not isinstance(programmer, Programmer):
        raise Exception("Bad type of programmer")
    device = load_class('devices', args.device)(programmer)
    if not isinstance(device, Device):
        raise Exception("Bad type of device")
    if args.action == 'erase':
        device.erase()
    else:
        match args.format:
            case 'bin':
                match args.action:
                    case 'program':
                        with open(args.file, 'rb') as fh:
                            device.write_data(0x00, fh.read())
                    case 'dump':
                        with open(args.file, 'wb') as fh:
                            fh.write(device.read_data(0x00, device.flash_size()))
            case 'hex':
                match args.action:
                    case 'program':
                        hp = hex_parser.HexParser()
                        def parse_record(rec):
                            hp.parse_record(rec)
                            if hp.address is not None and hp.data is not None:
                                device.write_data(hp.address, hp.data)
                        record = ''
                        with open(args.file, 'r') as fh:
                            for i in range(os.path.getsize(args.file)):
                                ch = fh.read(1)
                                if ch == '\n':
                                    continue
                                if ch == ':':
                                    if not record:
                                        continue
                                    parse_record(record)
                                    record = ''
                                else:
                                    record += ch
                            parse_record(record)

                    case 'dump':
                        raise Exception("Not supported")
            case _:
                raise Exception("Format have bad type")
    device.close()