

amplitudes = []

with open(r'tests\fpga_data.txt', 'r') as file:
    for line in file:
        print('Line: ', line)
        line = line.strip()
        print("Stripped line: ", line)
        if line.isnumeric():
            amplitudes.append(int(line))
