def parse_traceroutes(filename):
    """
    Returns a dictionary of destination IPs to a list of hops.
    """
    trace_dict = {}

    f = open(filename, 'r')
    for line in f:

        trace = [] #list to hold hops

        segments = line.split()
        dest = segments[1]
        num_hops = segments[3].strip()

        for i in range(0, int(num_hops)):
            hop_line = f.next()
            chunks = hop_line.split()

            hop_num = chunks[0][:-1]
            address = chunks[1]
            rtt = float(chunks[2])
            ttl = int(chunks[3].strip())

            hop = (hop_num, address, rtt, ttl)
            trace.append(hop)

        try:
            dest_traces = trace_dict[dest]
            dest_traces.append(trace)
        except KeyError:
            trace_dict[dest] = [trace]
            
    f.close()

    return trace_dict
