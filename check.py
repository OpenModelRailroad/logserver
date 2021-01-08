import bitstring


def decimal_to_binary(n):
    return '{:08b}'.format(n)


if __name__ == "__main__":
    praeambel = 0b11111111111111
    address = 5 & 0X7F
    bs = 0b01000000 | (4 & 0x0F) | (1 << 5)
    cs = address ^ bs

    dcc = "{} 0 {} 0 {} 0 {} 1".format(decimal_to_binary(praeambel), decimal_to_binary(address), decimal_to_binary(bs), decimal_to_binary(cs))

    # dcc = bitstring.BitArray(decimal_to_binary(praeambel))
    # dcc.append()
    # dcc.append(0b0)
    # dcc.append(decimal_to_binary(address))
    # dcc.append(0b0)
    # dcc.append(decimal_to_binary(bs))
    # dcc.append(0b0)
    # dcc.append(decimal_to_binary(cs))
    # dcc.append(0b1)

    print(praeambel)
    print(decimal_to_binary(praeambel))
    print(address)
    print(decimal_to_binary(address))
    print(bs)
    print(decimal_to_binary(bs))
    print(cs)
    print(decimal_to_binary(cs))

    print(dcc)
