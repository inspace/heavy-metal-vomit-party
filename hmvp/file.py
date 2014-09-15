def read_provider_customers(provider_customers_file):
    #from CAIDA 20130801.ppdc-ases.txt
    provider_customers = {}

    f = open(provider_customers_file)
    for line in f:
        line = line.strip()
        chunks = line.split()
        provider = chunks[0]
        provider_customers[provider] = chunks
    f.close()

    return provider_customers

def read_customer_providers(provider_customers_file):
    
    customer_providers = {}
    f = open(provider_customers_file)
    for line in f:
        line = line.strip()
        chunks = line.split()
    
        provider = chunks[0]
        
        for customer in chunks:
            try:
                customer_providers[customer].append(provider)
            except KeyError:
                customer_providers[customer] = [provider]
    f.close()
    
    return customer_providers

def read_digfile(dig_file):
    mapping = {}
    f = open(dig_file)
    for line in f:
        try:
            line = line.strip()
            chunks = line.split(',')
            client = chunks[0]
            mapping[client] = chunks[1:]
        except:
            sys.stderr.write('Error parsing line: %s\n' % line)
    f.close()
    return mapping

def read_prefixfile(prefix_summary):
    prefixes = {}
    f = open(prefix_summary)
    for line in f:
        line = line.strip()
        chunks = line.split()
        
        prefix = chunks[0]
        lat = float(chunks[1])
        lon = float(chunks[2])
        #countrycode = chunks[3]
        #asn = chunks[4]
        asn = chunks[3]
        try:
            asn = hmvp.ip.fix_asn(asn)
        except:
            pass

        #prefixes[prefix] = (lat, lon, countrycode, asn)
        prefixes[prefix] = (lat, lon, asn)
    f.close()

    return prefixes

def read_probefile(probesummary):
    probes = {}
    f = open(probesummary)
    for line in f:
        line = line.strip()
        chunks = line.split()

        probeid = chunks[0]
        asn = chunks[1]
        
        countrycode = chunks[8]
        lat = float(chunks[9])
        lon = float(chunks[10])

        probes[probeid] = (asn, countrycode, lat, lon)
    f.close()

    return probes

def read_googlefile(google_file, frontend_filter='all'):
    google = {}
    f = open(google_file)
    for line in f:
        line = line.strip()
        chunks = line.split()
        
        ip = chunks[0]
        asn = chunks[1]
        hostname = chunks[2]
        lat = float(chunks[3])
        lon = float(chunks[4])
        country = chunks[5]

        if frontend_filter == 'isp' and (asn == '36040' or asn == '15169'):
            continue
        elif frontend_filter == 'google' and (asn != '36040' and asn != '15169'):
            continue

        google[ip] = (asn, hostname, lat, lon, country)
    f.close() 

    return google 
