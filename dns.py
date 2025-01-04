from dnslib.server import DNSServer, BaseResolver, DNSHandler
from dnslib import RR, A, QTYPE, DNSRecord


#Your pi's local 
host = "192.168.29.37"
port = 53
BLOCKED_IP = "0.0.0.0"
#Read ad.txt for blocked domains
file =  open('ads.txt', 'r')
BLOCKED_DOMAINS = file.read().split('\n')
file.close()


class FilterResolver(BaseResolver):
    def resolve(self, request, handler):
        domain = str(request.q.qname).strip(".").lower()
        if(domain in BLOCKED_DOMAINS):
			#Respond with null ip
            resp = request.reply()
            resp.add_answer(
                RR(
                    rname=request.q.qname,
                    rtype=QTYPE.A,
                    rclass=1,
                    ttl=60,
                    rdata=A(BLOCKED_IP),
                )
            )
            return resp
        #Redirct to 8.8.8.8:53, Google's resolver server
        else:
            return DNSRecord.parse(request.send("8.8.8.8", 53))


if(__name__ == "__main__"):
    dns_server = DNSServer(FilterResolver(), port=port, address=host,logger=None)
    try:
        print(f"DNS Server active on {host}:{port}")
        dns_server.start()
    except KeyboardInterrupt:
        print("\n\Terminating server...")
        dns_server.stop()
	
