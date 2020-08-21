int = 32767

data = [int >> 8 & 0xff, int & 0xff]

print(bytearray(data))

convert = [data[0] << 8 | data[1]]
print(convert)
