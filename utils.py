def get_bit(decimal, N):
    mask = 1 << N
    if decimal & mask:
        return 1
    else:
        return 0

def set_bit(decimal,N,value):
    if value:
        new_decimal = decimal | 1 << N
    else:
        new_decimal = decimal & ~(1 << N)
    return new_decimal