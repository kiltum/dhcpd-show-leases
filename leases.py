#!/usr/bin/env python3
""" parse dhcpd.leases file to human-readable format """
import datetime

def parse_timestamp(raw_str):
    """ convert timestamp to datetime """
    tokens = raw_str.split()
    return datetime.datetime.strptime(" ".join(tokens[1:]), "%Y/%m/%d %H:%M:%S")

def timestamp_is_ge(t1, t2):
    """ stub """
    return str(t1) >= str(t2)

def timestamp_is_lt(t1, t2):
    """ stub """
    return str(t1) < str(t2)

def timestamp_is_between(t, tstart, tend):
    """ stub """
    return timestamp_is_ge(t, tstart) and timestamp_is_lt(t, tend)

def parse_hardware(raw_str):
    """ stub """
    return raw_str.split()[1]

def strip_endquotes(raw_str):
    """ stub """
    return raw_str.strip('"')

def identity(raw_str):
    """ stub """
    return raw_str

def parse_binding_state(raw_str):
    """ stub """
    return raw_str.split()[1]

def parse_next_binding_state(raw_str):
    """ stub """
    return raw_str.split()[2]

def parse_rewind_binding_state(raw_str):
    """ stub """
    return raw_str.split()[2]

def parse_leases_file(leases_file): # pylint: disable=R0912
    """ stub """
    valid_keys = {
        "starts": parse_timestamp,
        "ends": parse_timestamp,
        "tstp": parse_timestamp,
        "tsfp": parse_timestamp,
        "atsfp": parse_timestamp,
        "cltt": parse_timestamp,
        "hardware": parse_hardware,
        "binding": parse_binding_state,
        "next": parse_next_binding_state,
        "rewind": parse_rewind_binding_state,
        "uid": strip_endquotes,
        "client-hostname": strip_endquotes,
        "option": identity,
        "set": identity,
        "on": identity,
        "abandoned": None,
        "bootp": None,
        "reserved": None,
    }

    leases_db = {}

    lease_rec = {}
    in_lease = False
    in_failover = False

    for line in leases_file:
        if line.lstrip().startswith("#"):
            continue

        tokens = line.split()

        if len(tokens) == 0:
            continue

        key = tokens[0].lower()

        if key == "lease":
            if not in_lease:
                ip_address = tokens[1]

                lease_rec = {"ip_address": ip_address}
                in_lease = True

        elif key == "failover":
            in_failover = True
        elif key == "}":
            if in_lease:
                for k in valid_keys: # pylint: disable=C0206
                    if callable(valid_keys[k]):
                        lease_rec[k] = lease_rec.get(k, "")
                    else:
                        lease_rec[k] = False

                ip_address = lease_rec["ip_address"]

                if ip_address in leases_db:
                    leases_db[ip_address].insert(0, lease_rec)

                else:
                    leases_db[ip_address] = [lease_rec]

                lease_rec = {}
                in_lease = False

            elif in_failover:
                in_failover = False
                continue

        elif key in valid_keys:
            if in_lease:
                value = line[(line.index(key) + len(key)) :]
                value = value.strip().rstrip(";").rstrip()

                if callable(valid_keys[key]):
                    lease_rec[key] = valid_keys[key](value)
                else:
                    lease_rec[key] = True

    return leases_db


def lease_is_active(lease_rec, as_of_ts):
    """ stub """
    return timestamp_is_between(as_of_ts, lease_rec["starts"], lease_rec["ends"])

def select_active_leases(leases_db, as_of_ts):
    """ stub """
    retarray = []

    for ip_address in leases_db:
        lease_rec = leases_db[ip_address][0]
        if lease_is_active(lease_rec, as_of_ts):
            retarray.append(lease_rec)
    return sorted(retarray, key=lambda d: d['client-hostname'].lower())

with open("/var/lib/dhcp/dhcpd.leases", mode="r", encoding="utf-8") as file:
    leases = parse_leases_file(file)
    now_string = str(datetime.datetime.now(datetime.UTC)).split('.', maxsplit=1)[0]
    now = datetime.datetime.strptime(now_string, '%Y-%m-%d %H:%M:%S')

    report_dataset = select_active_leases(leases, now)

    print("+-----------------+-------------------+-------------+-------------------------------+")
    print("| IP Address      | MAC Address       | Expires in  | Hostname                      |")
    print("+-----------------+-------------------+-------------+-------------------------------+")

    for lease in report_dataset:
        print(
            "| "
            + format(lease["ip_address"], "<15")
            + " | "
            + format(lease["hardware"], "<17")
            + " | "
            + format(str(lease["ends"] - now), "<11")
            + " | "
            + format(lease["client-hostname"], "<30")
            + "|"
        )

    print("+-----------------+-------------------+-------------+-------------------------------+")
