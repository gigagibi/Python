import struct as s

def create_structure_d(binary_data, value):
    d1 = s.unpack('=i', binary_data[value:value+4])[0]
    d2 = s.unpack('=II', binary_data[value+4:value+12])

    return {
        'D1': d1,
        'D2': str(binary_data[d2[1]:d2[1] + d2[0]])[2:-1]
    }

def create_structure_e(binary_data, value):
    e1 = s.unpack('=b', binary_data[value:value+1])[0]
    e2 = s.unpack('=B', binary_data[value+1:value+2])[0]
    e3 = list(s.unpack('=8h', binary_data[value+2:value+18]))
    return {
        'E1': e1,
        'E2': e2,
        'E3': e3
    }


def f31(binary_data):
    structure = {}
    a1 = str(binary_data[4:11])[2:-1]
    structure['A1'] = a1

    c1 = s.unpack('=H', binary_data[11:13])[0]
    c2 = s.unpack('=q', binary_data[13:21])[0]
    c3 = s.unpack('=Q', binary_data[21:29])[0]
    b2 = s.unpack('=i', binary_data[29:33])[0]
    b3 = s.unpack('=d', binary_data[33:41])[0]
    b4 = s.unpack('=f', binary_data[41:45])[0]

    structure['A2'] = {
        'B1': {
            'C1': c1,
            'C2': c2,
            'C3': c3
        },
        'B2': b2,
        'B3': b3,
        'B4': b4
    }

    structure['A3'] = s.unpack('=B', binary_data[45:46])[0]

    a4a = s.unpack('=H', binary_data[46:48])
    a4 = create_structure_d(binary_data, a4a[0])
    structure['A4'] = a4

    structure['A5'] = [
        create_structure_e(binary_data, 48),
        create_structure_e(binary_data, 66),
        create_structure_e(binary_data, 84)
    ]

    return structure


# print(f31((b'ORE\xf3mkyohkm\xd2\x0f\x1f\xd0\xe5\x10W\xf3l)PO\xc6u|\x0e\xa61\xde\x8aP'
# b'\xc9\x98\x93%\x91Ay\xce?c\x83J?\xe1i\x00\x0c|\xb1*\xedIR\x8b\xa5(\xa2\xaf'
# b'\x07\x83\xdfY\x17\x95\x10h\r\xf3\xfe\x02\\\x08\x98\xd3 \xf8\x8be^\xbdR\x82'
# b'\x1e\x87QNgZx\xbe\xf5]\xbc\xb5\x8b\x88\xe0\xea\x0f;zok\xb2\xa4\x9d'
# b'^\x03\x00\x00\x00f\x00\x00\x00')
# ))