import requests
import json

name = "nc_dns"


class DNSZone(object):
    def __init__(self, name, ttl, serial, refresh, retry, expire, dnssecstatus):
        self.name = name
        self.ttl = ttl
        self.serial = serial
        self.refresh = refresh
        self.retry = retry
        self.expire = expire
        self.dnssecstatus = dnssecstatus

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class DNSRecord(object):
    __valid_types = ['A', 'AAAA', 'MX', 'CNAME', 'CAA', 'SRV', 'TXT', 'TLSA', 'NS', 'DS', 'OPENPGPKEY', 'SMIMEA']

    def __init__(self, hostname, type, destination, **kwargs):
        self.hostname = hostname
        self.type = type.upper()
        self.destination = destination
        self.priority = kwargs.get("priority", None)
        self.id = kwargs.get("id", None)
        self.deleterecord = kwargs.get("deleterecord", False)
        self.state = True

        if self.type not in self.__valid_types:
            raise TypeError("Invalid record type: {}".format(self.type))

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, ', '.join(
            '{}={!r}'.format(k, v)
            for k, v in self.__dict__.items()
            if v is not None
        ))

    __repr__ = __str__

    def __eq__(self, other):
        if not isinstance(other, DNSRecord):
            return False

        result = self.hostname == other.hostname and self.destination == other.destination and self.type == other.type

        if self.type == 'MX' and other.type == self.type and self.priority:
            result = result and int(self.priority) == int(other.priority)

        if self.id and other.id:
            result = result and self.id == other.id

        return result


class Client(object):
    __endpoint = "https://ccp.netcup.net/run/webservice/servers/endpoint.php?JSON"
    __api_session_id = None

    def request(self, action, **kwargs):
        params = kwargs.get("params", {})
        params.update({
            "apikey": self.__api_key,
            "customernumber": self.__customer,
        })

        if "apipassword" not in params and not self.__api_session_id:
            raise Exception("Request was called on closed connection")

        if self.__api_session_id:
            params.update({"apisessionid": self.__api_session_id})

        response = requests.post(
            self.__endpoint,
            data=json.dumps({
                "action": action,
                "param": params
            }),
            timeout=self.__api_timeout
        )

        if response.ok:
            data = response.json()

            if data['status'] == 'success':
                return data
            # empty dns zone
            elif data['statuscode'] == 5029:
                return []
            else:
                raise Exception("{} ({})".format(data['longmessage'], data['statuscode']))
        else:
            raise Exception("{} ({})".format(response.reason, response.status_code))

    def logout(self):
        self.request("logout")
        self.__api_session_id = None

    def login(self):
        data = self.request("login", params={"apipassword": self.__api_password})
        self.__api_session_id = data['responsedata']['apisessionid']

    def add_dns_record(self, domain, record):
        return self.update_dns_records(domain, [record])

    def update_dns_record(self, domain, record):
        if not record.id:
            raise ValueError("Missing id of record to update")

        return self.update_dns_records(domain, [record])

    def update_dns_records(self, domain, records):
        if not all(isinstance(r, DNSRecord) for r in records):
            raise TypeError("Record has to be instance of DNSRecord")

        data = self.request("updateDnsRecords", params={
            "domainname": domain,
            "dnsrecordset": {"dnsrecords": [record.__dict__ for record in records]}
        })

        if 'responsedata' not in data:
            return []

        return [DNSRecord(**r) for r in data['responsedata']['dnsrecords']]

    def dns_record_exists(self, domain, record):
        return record in self.dns_records(domain)

    def dns_record(self, domain, record):
        records = self.dns_records(domain)

        for r in records:
            if record == r:
                return r

        return None

    def delete_dns_record(self, domain, record, ignore_unknown=True):
        if not record or not record.id:
            raise ValueError("Missing id of record to update")

        record.deleterecord = True

        try:
            return self.update_dns_records(domain, [record])
        except Exception as ex:
            if not ignore_unknown:
                raise ex
            else:
                return []

    def delete_dns_records(self, domain, records):
        for r in records:
            r.deleterecord = True

        return self.update_dns_records(domain, records)

    def dns_records(self, domain):
        data = self.request("infoDnsRecords", params={"domainname": domain})

        if 'responsedata' not in data:
            return []

        return [DNSRecord(**r) for r in data['responsedata']['dnsrecords']]

    def update_dns_zone(self, domain, zone):
        if not isinstance(zone, DNSZone):
            raise TypeError("Zone has to be instance of DNSZone")

        self.request("updateDnsZone", params={
            "domainname": domain,
            "dnszone": zone.__dict__
        })

    def dns_zone(self, domain):
        data = self.request("infoDnsZone", params={"domainname": domain})
        return DNSZone(**data['responsedata'])

    def __init__(self, customer, api_key, api_password, timeout=5):
        self.__customer = customer
        self.__api_key = api_key
        self.__api_password = api_password
        self.__api_timeout = timeout

        self.login()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.logout()
