import sys


def convert_size_to_bytes(size):
    size = size.replace(' ', '')
    multipliers = {
        'kb': 1024,
        'mb': 1024*1024,
        'gb': 1024*1024*1024,
        'tb': 1024*1024*1024*1024
    }

    for suffix in multipliers:
        if size.lower().endswith(suffix):
            return float(size[0:-len(suffix)]) * multipliers[suffix]
    else:
        if size.lower().endswith('b'):
            return float(size[0:-1])

    try:
        return float(size)
    except ValueError: # for example "1024x"
        print('Malformed input!')
        exit()


with open(sys.argv[1], 'r') as infile:
    lines = infile.read().replace('d, ', 'd,-').replace('s, ', 'd,-').splitlines()

lines = [lines[i] for i in range(2, 180, 3)]

throughputs = lines[:30]
latencies = lines[30:]
throughputs = iter(throughputs)
latencies = iter(latencies)

read_throughput = 0
write_throughput = 0

read_latency = 0
write_latency = 0

tables = open(sys.argv[2], 'w')
tables.write("Block Size, Read Throughput, Read Latency\n")
for i in range(9, 14):
    for j in range(3):
        read_throughput += float(convert_size_to_bytes(next(throughputs).split('-')[2][:-2]))
        read_latency += float(next(latencies).split('-')[1][:-2])
    tables.write("%i, %.0f, %.4f\n" % (2 ** i, (read_throughput/1024) / 3.0, read_latency / 3.0))
tables.write('\n')
tables.write("Block Size, Write Throughput, Write Latency\n")
for i in range(9, 14):
    for k in range(3):
        write_throughput += float(convert_size_to_bytes(next(throughputs).split('-')[2][:-2]))
        write_latency += float(next(latencies).split('-')[1][:-2])
    tables.write("%i, %.0f, %.4f\n" % (2 ** i, (write_throughput/1024) / 3.0, write_latency / 3.0))
tables.close()
