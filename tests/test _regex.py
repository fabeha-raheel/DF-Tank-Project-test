import re
import numpy as np

# Extracting start frequency

# startbit = r"11111111 >> ([0-9]*)"
# test_line = "11111111 >> 400000000"

# result = re.search(startbit, test_line)

# print(result.groups()[0])

# Extracting end frequency and No of samples
# stopSequence = r"^([0-9]*) >> ([0-9]*)$"
# test_line = "5730 >> 5900000000"

# result = re.search(stopSequence, test_line)

# print(result.groups())

x = np.arange(start=400000000, stop=5900000000, step=959860.3839441536)
print(len(x))