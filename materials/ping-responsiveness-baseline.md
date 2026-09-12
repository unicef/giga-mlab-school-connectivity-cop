# Inward Probe Responsiveness: An Empirical Baseline

A measured baseline for the inward-probing design in
[`ping-measurements-methodology.md`](./ping-measurements-methodology.md).

**Data:** 606,129 M-Lab traceroute measurements from 137,734 Giga
Meter client IPs across 25 countries, August 2026.

## What is actually being measured

**This is a pingable-proxy, not ping.** The signal is `reach_dest` from M-Lab's traceroutes: 
the trace's destination *is* the client, so it records whether
the school's public egress address answered the probe that terminated at it. It
is traceroute-destination reachability, **not ICMP echo**. No ICMP echo dataset
exists for these addresses, so this is the closest available evidence, and it
should be read as a *lower bound proxy* for inbound reachability rather than as
a ping success rate.

Two granularities are reported, and the distinction carries the finding:

| Column | Meaning |
|---|---|
| **Responsive (IP)** | The school's own egress address answered. |
| **Responsive (ASN)** | The forward path reached the school's *network*, without the address necessarily answering. |

The ASN signal comes from HERMES's `is_reaching_dst_asn`, which — despite the
name — means the path reached the **client's** ASN, not the server's. 

An IP counts as responsive in a month when at least half of its measurements
answered.

## The finding: the network is reachable, the host is not

The median country has **6.5%** of its client IPs answering directly,
while **56.0%** have their network reached. The probe is arriving at the
school's ISP and dying at the last hop.

That is the signature of exactly what the methodology note predicted —
CGNAT, edge firewalls, and consumer CPE that drops unsolicited inbound traffic
— and not of a backbone or routing failure. It has a concrete design
consequence: **an inward-probing tier aimed at school egress addresses would
fail for the large majority of schools in most of these countries**, while
probing *to the school's ISP* would largely succeed and tell you much less.

Where the gap is widest, the school network is reachable but the endpoint is
firewalled off almost entirely:

- **Kyrgyzstan** — 0.0% of IPs answer, 100.0% of networks reached (100.0% gap, 49 IPs)
- **Sri Lanka** — 14.5% of IPs answer, 84.4% of networks reached (69.9% gap, 46,674 IPs)
- **Fiji** — 6.5% of IPs answer, 72.1% of networks reached (65.6% gap, 2,400 IPs)

Kyrgyzstan tops that list on 49 IPs, so read it as directional; Sri Lanka's
gap rests on 46,674 IPs and is the solid case.

Where it is narrowest, something different is happening — the path is not
reaching the network either, which is a reachability or routing story rather
than a filtering one, and is worth investigating separately:

- **Saint Lucia** — 0.0% of IPs answer, 0.0% of networks reached (0.0% gap, 18 IPs)
- **Zambia** — 0.5% of IPs answer, 0.6% of networks reached (0.1% gap, 805 IPs)
- **Dominica** — 19.6% of IPs answer, 25.0% of networks reached (5.4% gap, 56 IPs)

Saint Lucia's zero gap is two zeros on 18 IPs rather than a finding.

Zambia is the clearest case of the second pattern, and the only one with a
denominator worth trusting: on 805 IPs, the network is reached
0.6% of the time — so the probe is not
dying at a school firewall, it is not arriving at all. That is a different
problem from the one inward probing would need to solve, and worth a look on
its own.

## Results by country, August 2026

| Code | Country | IPs measured | Responsive (IP) | Responsive (ASN) | Gap | Responsive (IP, per-measurement) | Measurements |
|---|---|---|---|---|---|---|---|
| NA | Namibia | 445 | 54.4% | 98.4% | 44.0% | 85.5% | 3,227 |
| MD | Moldova | 572 | 52.6% | 63.6% | 11.0% | 80.9% | 4,234 |
| KE | Kenya | 18,328 | 27.4% | 77.4% | 50.0% | 37.2% | 98,857 |
| BA | Bosnia and Herzegovina | 6,493 | 27.3% | 64.2% | 36.9% | 28.3% | 15,417 |
| AL | Albania | 7,014 | 20.9% | 34.8% | 14.0% | 22.1% | 24,158 |
| DM | Dominica | 56 | 19.6% | 25.0% | 5.4% | 34.6% | 179 |
| TT | Trinidad and Tobago | 372 | 19.4% | 71.5% | 52.2% | 24.8% | 1,354 |
| LS | Lesotho | 167 | 18.0% | 59.3% | 41.3% | 18.3% | 503 |
| LK | Sri Lanka | 46,674 | 14.5% | 84.4% | 69.9% | 10.5% | 104,552 |
| BZ | Belize | 342 | 8.5% | 64.0% | 55.6% | 23.5% | 1,891 |
| GD | Grenada | 25 | 8.0% | 36.0% | 28.0% | 4.6% | 152 |
| KZ | Kazakhstan | 3,241 | 7.2% | 63.3% | 56.1% | 13.8% | 10,461 |
| FJ | Fiji | 2,400 | 6.5% | 72.1% | 65.6% | 4.9% | 9,780 |
| MN | Mongolia | 3,639 | 6.3% | 56.0% | 49.7% | 17.8% | 17,647 |
| BW | Botswana | 724 | 5.4% | 62.4% | 57.0% | 9.3% | 3,342 |
| HN | Honduras | 792 | 5.3% | 12.4% | 7.1% | 7.9% | 2,140 |
| ZA | South Africa | 28,645 | 5.1% | 22.4% | 17.2% | 5.5% | 71,190 |
| ME | Montenegro | 1,440 | 5.1% | 51.2% | 46.1% | 6.2% | 6,588 |
| UZ | Uzbekistan | 13,920 | 4.5% | 39.5% | 35.0% | 3.8% | 221,761 |
| RW | Rwanda | 699 | 3.0% | 40.2% | 37.2% | 6.2% | 1,410 |
| MW | Malawi | 862 | 2.0% | 34.7% | 32.7% | 3.6% | 4,784 |
| ZM | Zambia | 805 | 0.5% | 0.6% | 0.1% | 0.4% | 2,274 |
| KG | Kyrgyzstan | 49 | 0.0% | 100.0% | 100.0% | 0.0% | 80 |
| LC | Saint Lucia | 18 | 0.0% | 0.0% | 0.0% | 0.0% | 40 |
| VC | Saint Vincent and the Grenadines | 12 | 0.0% | 33.3% | 33.3% | 0.0% | 108 |

Sorted by IP-level responsiveness. The **per-measurement** column pools every
probe instead of giving each IP one vote; where it diverges sharply from the IP
column, a small number of high-volume IPs dominate that country's traffic. Both
are reported because quoting either alone invites a Simpson's-paradox reading.

## Limits worth carrying into any use of this table

- **Proxy, not ping.** Traceroute destination reachability, not ICMP echo. A
  host that drops ICMP echo but answers the terminating traceroute probe (or
  vice versa) is counted differently than a real ping census would count it.
- **Counts are IP-keyed, not school-keyed.** The IP-to-school ratio across this
  corpus runs 0.92× to 11.6× with no consistent direction, so these are counts
  of addresses, not of schools.
- **Thin denominators in small countries.** Saint Vincent and the Grenadines
  rests on 12 IPs and Saint Lucia on 18; treat single-digit-IP rows as
  directional only.
- **Observation is conditional on the school being online.** Only schools that
  were powered, connected and running the agent contribute at all, so this
  says nothing about schools that never appear.

## Reproducing

Generated by `scripts/pingability` in the GIGA traceroute analysis repo, from
`mlab-collaboration.hermes_union.giga_meter_measurements`, deduplicated on
`(id, src, month)` with the month taken from `window_start`:

```
PYTHONPATH=. python -m scripts.pingability --month 2026-08
```

