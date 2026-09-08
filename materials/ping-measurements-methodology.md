# Ping Measurements and the Future of Giga's Measurement Capability

* Version: 1
* First shared: 2026-09-07
* Status: notes / draft
* Author(s): Loqman Salamatian `loqman@measurementlab.net`

These notes sit primarily in _Workstream 1: Improving measurement tools_,
Task 1.1 of the [research agenda](../research_agenda.md), and are a companion
to [`qoe-measurements-design.md`](./qoe-measurements-design.md). Part 2 also
touches Workstream 4 (new insights from existing measurement data) and Part 3
is offered in the spirit of Workstream 5 (BYOI).

## Context

Giga's current measurement backbone is the Giga Meter: a Windows desktop
application that runs up to four speed tests per day from a school computer,
feeding results into Giga Maps. This gives a periodic snapshot of capacity
(download/upload Mbps) but says little about availability, consistency, or
whether the connection is actually usable for digital learning. These notes
sketch how ping/latency measurement could be designed deliberately, and how
the broader measurement capability could evolve.

## Part 1: Using ping measurements to understand user performance

### Why ping at all

Ping is the cheapest measurement that exists: a few bytes per probe versus
tens to thousands of megabytes per speed test. Speed tests can only ever be
sparse samples; pings can be near-continuous. And latency, jitter, and packet
loss are sometimes better predictors of the _experienced_ quality of
interactive applications (video lessons, collaborative tools, cloud-based
learning platforms) than headline throughput is. A school with 20 Mbps and
stable 40 ms RTT might be more usable than one with 100 Mbps and 600 ms of
bufferbloat under load.

### From where (vantage points and targets)

The measurement architecture should be thought of as probing _path segments_,
not just "the Internet":

**Source: in-school agent.** Today that's the Giga Meter app on PCs; longer
term it should be the school router/gateway or a dedicated always-on probe
(see Part 2). The source should sit as close to the access link as possible so
measurements reflect the school's connection, not one PC's Wi-Fi.

**Targets at increasing path depth:**

1. School gateway / first hop (isolates the LAN/Wi-Fi)
2. ISP first router (isolates the last mile)
3. In-country anchors, national IXP, government data centre, or in-country CDN
   node (isolates the national backbone)
4. Regional CDN edges, e.g. nearest Cloudflare PoP (isolates international
   transit)
5. A small set of actual educational platforms/services in use in that country

**Inward probing.** Complement school-originated pings with probes _toward_
schools from external vantage points (Cloudflare's network, RIPE Atlas
anchors, a Giga measurement cloud). This detects outages even when the school
agent itself is offline and can't report.

Differential analysis across these targets turns ping from a single number
into a fault-localization tool: if RTT to the ISP first hop is fine but RTT to
the national anchor has blown up, the problem is the backbone, not the
school's link, which changes who you call and what the policy conclusion is.

### How often (sampling design)

* **Continuous low-rate heartbeat:** one probe every 1–5 minutes during school
  hours. This is the uptime/availability signal: a far better one than "did
  today's speed test run."
* **Periodic dense bursts:** e.g. 30–60 seconds at 1 probe/second a few times
  per day. Jitter and packet loss can't be estimated from sparse pings; they
  need bursts.
* **Idle vs. loaded sampling:** measure a baseline RTT before school hours and
  compare against RTT during peak classroom usage (and during the speed test
  itself). The delta is "latency under load" / bufferbloat.
* **Adaptive scheduling:** densify probing automatically when anomalies appear
  (rising loss, RTT inflation), back off when stable, to conserve data and
  power on constrained links.

### What for (the use cases the data serves)

1. **Availability/uptime accounting.**
2. **Usability classification.** Map (RTT, jitter, loss) against thresholds
   per use case: e.g. video conferencing roughly needs <150 ms RTT, <30 ms
   jitter, <1% loss; cloud document editing tolerates more. This is
   essentially IQB.
3. **Congestion and capacity-adequacy detection.** Recurring diurnal latency
   inflation indicates an undersized or oversubscribed link even when speed
   tests at quiet times look fine.
4. **Fault localization** via the multi-target design above, separating school
   LAN issues, last-mile faults, backbone problems, and international transit
   congestion.
5. **SLA verification.** Write latency, loss, and availability targets (not
   just Mbps) into ISP contracts, and use independent school-side measurement
   as the enforcement evidence. This is a lever Giga can hand to ministries
   during procurement.
6. **Outage forensics.** Correlating ping-derived outage windows across
   schools on the same ISP/region reveals systemic vs. local failures.

### Caveats to design around

* ICMP is often deprioritized or rate-limited by routers; supplement with TCP
  handshake RTT, UDP probe, or HTTPS time-to-first-byte so results survive
  ICMP policy weirdness.
* CGNAT and firewalls block inbound probes to many schools; inward probing
  needs cooperation (keepalive sessions from the agent, or ISP-side
  reflectors).
* A ping from one desktop over Wi-Fi conflates the LAN with the WAN, another
  argument for moving the agent to the gateway.
* Sampling bias: data only arrives from schools that are powered, online, and
  have the agent running. The absence of data is itself a signal that needs
  interpretation (see power disambiguation below).

## Part 2: Evolving measurement capability beyond speed tests

### Why speed tests alone might be insufficient

They are episodic (4/day misses most of the day), heavy on metered/satellite
links where data costs money, sensitive to test-server placement, dependent on
a Windows PC being switched on, and they measure _peak attainable capacity_:
not what users experience and not whether it's sufficient for the number of
students behind it.

### Direction 1: From capacity to experience

* Adopt **responsiveness under working conditions** (latency-under-load /
  RPM-style metrics) as a first-class indicator alongside Mbps.
* Run **lightweight synthetic transactions** that mirror real educational use:
  DNS resolution time, TTFB to the national learning platform, fetch time for
  a reference page, a short simulated video-streaming or video-call session
  scored for startup delay, sustained quality, and stalls. These cost a
  fraction of a speed test and map directly to classroom experience.

### Direction 2: Move the vantage point off the desktop

The single biggest structural upgrade: shift from a Windows app on someone's
PC to an **always-on agent at the network edge**, on the school router/CPE or
a cheap dedicated probe (Raspberry Pi-class hardware with battery backing).
Benefits: 24/7 visibility, measures the whole school rather than one machine.

### Direction 3: Add passive measurement

From the gateway, collect privacy-preserving aggregates: total bytes,
concurrent device counts, link utilization over time, per-protocol /
per-destination-category flow stats. This answers questions active tests
can't: Is the link actually being used? Is capacity the binding constraint, or
is utilization low for other reasons (devices, electricity, skills)? How many
simultaneous users does the link really serve? Passive utilization data plus
active QoE probes together describe both supply and demand.

### Direction 4: Multi-source data fusion

No single vantage point is trustworthy alone. Fuse: school-side agent data,
Cloudflare's network-side tests, M-Lab NDT results, ISP-side telemetry,
satellite operator telemetry, and regulator/QoS datasets. Cross-validation
between school-side and network-side measurements also defends against gaming
and misconfiguration.

### Direction 5: From metrics to sufficiency

Move reporting from raw Mbps to meaningful-connectivity indicators:
per-student capacity (Mbps per concurrent learner), "can N classrooms stream
simultaneously," % of school hours the link met the video-conferencing
usability threshold. These are the numbers ministries can plan and budget
against, and they make Giga Maps less descriptive.

### Direction 6: Operational intelligence

With continuous time series in hand: anomaly detection that flags degradation
before outright failure, automated ticketing/escalation to ISPs with
localization evidence attached, fleet-level views (e.g., all schools on ISP X
in region Y degraded), and predictive maintenance for connectivity hardware.

### A plausible sequencing

1. **Near term:** add continuous ping/latency heartbeats and
   latency-under-load to the existing Giga Meter.
2. **Medium term:** pilot router/probe-based agents in a few countries; add
   synthetic QoE transactions; write latency/availability SLAs into new
   connectivity procurements.

## Part 3: Beyond best practice, novel directions

Parts 1 and 2 are traditional network engineering, but they answer a question
the field has been answering for twenty years: "how is the network
performing?" The novelty space opens up when the question itself changes. Four
reframes, each of which would be new not just for Giga but for internet
measurement generally.

### Reframe A: Measure learning, not links

**The connectivity-to-learning elasticity.** Nobody on earth has a dataset
that links network quality to educational outcomes at scale. Giga is uniquely
positioned to build it, because it sits between ministries (EMIS data,
learning platforms, attendance, assessment results) and networks (per-school
QoS time series). Join the two and you can estimate: how does lesson
completion, platform engagement, or teacher usage respond to latency, jitter,
uptime, capacity? The output is an _evidence-based sufficiency threshold_
(e.g., "below X uptime during teaching hours, digital curriculum usage
collapses; above Y Mbps/student, returns flatten"). Today's thresholds (the
ITU/Giga Mbps targets) are expert guesses. This would replace them with
measured reality, and it would be a first in the field.

### Reframe B: Measure money, not Mbps

**Measurement as financial settlement.** The deepest problem in school
connectivity is ISP incentives: providers get paid whether or not the link
works well. Turn the measurement system into a _settlement layer_:
independently attested uptime/QoE data (cross-validated school-side +
network-side, tamper-evident) against which payments execute automatically.
Pay-for-performance contracts, results-based financing, even connectivity
bonds whose coupons depend on measured availability across a school portfolio.
The novel artifact is a trusted measurement oracle. Giga's position as a
neutral UNICEF/ITU entity is exactly what makes the oracle credible; no
commercial measurement company can play this role.

**The measurement dividend.** A fleet of millions of georeferenced vantage
points in the world's least-measured regions has real commercial value (CDN
placement, ISP planning). A structured, privacy-safe data product whose
revenue flows back into school connectivity inverts the usual model:
measurement could start co-financing the mission.

### Reframe C: Measure what didn't happen

**Suppressed-demand sensing.** Speed tests measure supply but do not measure
_thwarted demand_. From the gateway, count the failures: connection attempts
that timed out, video sessions abandoned in the first 30 seconds, DNS lookups
that never resolved, retry storms, downloads started and never finished.
Aggregate into an index per school, a counterfactual measurement of what usage
would be if the network weren't the constraint. This could be the number that
justifies upgrades. It also distinguishes the two failure modes that look
identical in utilization data: low usage because the link is bad vs. low usage
because demand isn't there (devices, electricity, training).

**Pre-connectivity measurement.** Today Giga can only measure schools that are
already connected. Build also measurement for the unconnected: ambient
mobile-coverage probing around school coordinates (crowdsourced signal data,
low-cost spectrum sensing on a solar probe), LEO visibility modeling,
predicted QoE per candidate technology. Procurement decisions get made against
measured radio reality rather than coverage maps that are known to be
inaccurate in remote areas.

### Reframe D: Measurement that acts and serves beyond schools

**Schools as a public internet observatory.** Giga's fleet would be the
largest set of fixed, neutral, georeferenced measurement points in precisely
the regions where the internet is least observed. Opened carefully
(privacy-safe, school-level), it becomes civic infrastructure that can support
national outage detection, disaster-response situational awareness (which
regions still have connectivity after a cyclone), regulatory evidence on
whether ISPs deliver what rural customers pay for, and research data on
Internet resilience in the Global South. The school could become the
measurement _instrument_ for its whole community — consistent with Giga's
"school as community anchor" model.
