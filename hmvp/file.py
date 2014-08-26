
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

def read_googlefile(google_file):
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

        google[ip] = (asn, hostname, lat, lon, country)
    f.close() 

    return google 
