def f22(x):
    q = "0"
    binary = str(bin(x))[2:]
    if len(binary) < 32:
        q = q * (32 - len(binary))
        binary = q + binary
    e = binary[-32:-31]
    d = binary[-31:-28]
    c = binary[-28:-13]
    b = binary[-13:-10]
    a = binary[-10:]
    s = int(e + b + a + c + d, 2)
    return s