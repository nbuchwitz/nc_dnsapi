# nc_dnsapi
A simple API wrapper for the netcup DNS API

```python
import nc_dnsapi

customer = 123456
api_key = "your-personal-api-key"
api_password = "your-private-api-password"

with nc_dnsapi.Client(customer, api_key, api_password) as api:
    # fetch records
    records = api.dns_records("example.com")
    print(records)
    
    # fetch zone details
    zone = api.dns_zone("example.com")
    print(zone)
    
    # update single record
    api.update_dns_record("example.com", DNSRecord("my-hostname", "A", "127.0.0.2", id=108125))
    
    # update list of records
    api.update_dns_record("example.com", [ DNSRecord("my-hostname", "A", "127.0.0.2", id=108125), 
        DNSRecord("my-hostname2", "A", "127.0.0.2", id=108126)])
        
    # delete record
    api.delete_dns_record("example.com", DNSRecord("my-hostname", "A", "127.0.0.2", id=108125))
    
    # add record
    api.add_dns_record("example.com", DNSRecord("another-host", "AAAA", "::1"))

    # update zone
    zone = api.dns_zone("example.com")
    zone.refresh = 3600
    api.update_dns_zone("example.com", zone)
```
