# value = 200
# # hex_value = hex(1000)
# hex_value = '{:04x}'.format(value)
# hex_value = hex(hex_value)
# print(hex_value)

value1 = 0x61a8
print(type(value1))
value = 200
hex_value = int('{:04x}'.format(value), 16)
# print(type(hex_value))
# print(value1+hex_value)