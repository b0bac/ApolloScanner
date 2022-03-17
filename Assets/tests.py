import dns.resolver

result = dns.resolver.resolve("www.baidu.com", "CNAME")
for item in result.response.answer:
    if item.rdtype == 5:
        for c in item:
            print(c)