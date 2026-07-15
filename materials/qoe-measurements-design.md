# QoE Measurement Suite for Learning-Ready Connectivity

*Status:* **draft** | current | needs update | obsolete  
*Author(s):* Simone Basso `sbs@measurementlab.net`

## Goal

Define and measure "learning-ready" connectivity for Giga's Connectivity
Credits program. The target is not raw speed but whether a school's
connection supports real educational use cases: browsing learning platforms,
streaming educational video, and interactive sessions.

## Core Principles

The design rests on three ideas:

1. **Multi-layer measurements ordered by cost.** Lightweight, latency-dominated
probes run frequently; heavyweight, bandwidth-dominated tests run less
often. Each layer captures a distinct aspect of quality.

2. **Descriptive methodology.** Build empirical distributions and plot
quantiles over time. No reductive pass/fail thresholds. For Connectivity
Credits or IQB-Edu, we would then need to collapse this into a number.

3. **API-driven measurement control.** This document defines measurement
capabilities and the Giga API (umbrella term to describe the API/APIs that
Giga Meter uses to communicate with the Giga backend) should dynamically
configure what each Meter instance runs, when, and how often. Giga Meter
instances that do not support a given measurement should just skip it (as
opposed to, say, refusing to run). This separates "what can we measure"
(mechanism) from "what we should measure" (policy). Crucially, the policy
can change more frequently than the mechanism.

## Vantage Points

Measurements can run from the end-user device or from the router. From
the device, we capture the full student experience including Wi-Fi.
From the router, we isolate the ISP-provided link. Both together allow
differencing out the Wi-Fi contribution. If only one is possible, prefer
the device: Giga assesses whether students can learn, not whether the
ISP link looks fine while Wi-Fi degrades the experience. When both run,
they should not overlap — e.g., device measures during odd hours, router
during even hours — to avoid competing for bandwidth.

## Disruption Tiers

Each measurement has a disruption potential (i.e., how much it can
disrupt other internet users or other measurements) that determines
how aggressively it can be scheduled:

**Interactive (non-disruptive).** Negligible bandwidth. DNS, TLS, HTTP
fetches (layers 1-3).

**Streaming (may disrupt).** Sustained moderate bandwidth. Constant-bitrate
streaming (layer 4).

**Bulk (likely disruptive).** Saturates the link. ndt7, MSAK (layers 5, 7).

The Giga API uses these tiers when configuring measurement policy — e.g.,
interactive probes can run frequently on metered connections where bulk
tests would be wasteful.

## Measurement Layers

Ordered from cheapest (most frequent) to most expensive (least frequent).

### 1. DNS Resolution over UDP

Pure latency measurement. Round-trip time dominates; bytes are negligible.
Characterizes the network latency required to resolve a domain name. Uses
existing public resolvers (e.g., Google, Cloudflare) as targets and could
also potentially discover the default resolver used by the device and
use it directly. The main trade off: using the default DNS captures
the actual user experience. Alternative DNS servers speak volumes to
connectivity with important providers (Google, Cloudflare, Quad9) and
it is a cheap “ping” measurement. Doing both is actually important to
know whether there is no DNS interception (see below).

Caveat: ISPs could capture and transparently route DNS-over-UDP queries
but there are techniques to address this such as
`whoami.v4.powerdns.org` and `whoami.v6.powerdns.org` to determine
the *actual* resolver used by queries (regardless of configuration).

BTW: errors (such as frequency of timeouts) is also very informative here.

### 2. TLS Handshake and DNS-over-HTTPS

Small sequential exchanges where severe degradation is clearly detectable
(as shown by OONI's throttling research). Uses existing public endpoints
as targets. Impossible to fully MITM this unless there are custom CAs
but we can always bundle our own CA. The overall latency should be more
noisy and greater than the DNS-over-UDP one.

Re: bundling our own CA, worth having a conversation regarding whether
schools choose to (or are required to) install specific antivirus software
or middleboxes for security. In general, the presence of these devices,
especially if they decrypt TLS traffic and/or mess with TCP, could be
an issue both for measuring QoE and performance.

The main metrics are (1) time to complete the transaction and (2) bytes
sent and received, so that we can estimate whether latency dominates
(expected) or bandwidth dominates.

BTW: errors (such as frequency of timeouts) is also very informative here.

### 3. HTTP/2 Web Fetches

Fetch multiple small resources over a single TCP connection from the
same origin, modeling how modern browsing works. The mechanism is the
same regardless of target; the choice of target is policy:

- **Learning platforms**: a curated list of publicly accessible landing
pages. Richest QoE signal for the education use case, but content changes
over time and CDN behavior varies. Login-protected content remains out of
reach for active measurements. The general approach — actively fetching
resources from a curated target list — has precedent in OONI's web
connectivity measurements.

- **Controlled origin**: a well-provisioned server serving fixed assets.
Reproducible baseline, isolates network quality from server-side
variability.

Both can coexist in the same target list. Uses existing public infrastructure
or a controlled test server depending on target selection.

The most important metrics here are: (a) TTFB (time to the first byte),
which roughly captures how much latency there is between trying to open
a resource and getting the first byte that is actual content and not
overhead; (b) size and time required to fetch the resource, which informs
us of how much one needs to wait and about the download speed (indirectly).

BTW: errors (such as frequency of timeouts) is also very informative here.

### 4. Constant-Bitrate Sustained Streaming

"Can this connection hold a video call without stalls?" Fixed bitrate
target (e.g., 2 Mbps for video). No adaptive bitrate logic — ABR algorithms'
internal dynamics confound the measurement, making it difficult to
separate network behavior from algorithm behavior. The primary QoE
signals are application-layer stall events (receive buffer underruns)
and their duration, supplemented by `tcp_info` diagnostics (RTT variance,
retransmissions, congestion window dynamics) to explain why stalls occur
(see the `tcp_info` caveat under layer 5). Implementation path: a new
MSAK endpoint with fixed bandwidth target and application-level pacing
over BBR. Requires new work but the mechanism is \~straightforward.

### 5. ndt7 Single-Stream Capacity

Single TCP stream over \~10 seconds. Provides the baseline capacity
metric. Already deployed via Giga Meter. Includes both download
and upload measurements; the upload test covers the "how long to upload
an assignment" use case. Two distinct metrics can be extracted: (a)
unfiltered average including initial transient, reflecting actual user
experience when starting a download or stream; (b) filtered estimate
excluding transient and spikes, approximating steady-state capacity. For
learning-ready assessment, (a) better captures the actual user experience;
for capacity planning, (b) is more informative. A third derived signal is
latency under load (bufferbloat): the difference between min RTT and RTT
during the test, available from `tcp_info` samples. Caveat: ndt7 uses
BBR, which is designed to minimize queue buildup. The RTT inflation
observed during a BBR-based test is a lower bound on the bufferbloat
that loss-based congestion control (e.g., CUBIC, still the default on
most platforms) would trigger. A clean reading does not guarantee the
path is bufferbloat-free for typical application traffic. More broadly,
`tcp_info` metrics reflect what the local TCP stack observes, which may
differ from the end-to-end path when a Performance Enhancement Proxy
(PEP) or other mid-path TCP termination is present. PEPs are common on
radio links, including satellite and mobile networks. In such cases,
BBR's estimated bandwidth and RTT describe only the leg between the
server and the proxy, not the full path to the client. Goodput remains
the authoritative end-to-end signal; kernel-level metrics should be
treated as informational and complementary.

### 6. Traceroute

Path characterisation. Useful for diagnosing routing anomalies and
understanding path composition, but not a direct QoE metric. Complementary
and diagnostic. Already implemented for server-to-client. Requires an
implementation from Giga Meter to specific targets.

We empirically confirmed that Giga Meter can run traceroute on Windows
devices without administrator privileges. The same holds for Linux. I
don’t have a macOS to test. On mobile devices this used to be complex but
the situation may have changed since the Measurement Kit days (2014-2020),
so probably it makes sense to investigate again.

### 7. MSAK Multi-Stream Capacity

Multiple parallel streams to estimate aggregate capacity. Most
bandwidth-expensive and network-disruptive test. Information content is
diagnostic: settles whether a single-stream test is bottlenecked by the
connection or by TCP congestion control dynamics on the specific path.
Not a QoE measurement. Helps to figure out the overall school capacity.

## Architectural Decisions

**End-to-end measurement.** Servers at IXPs and data centers (M-Lab
placement model), not inside ISP networks (preferably). Students access
content hosted outside their ISP; end-to-end measurements reflect this.
Router measurements could also happen but we should prefer end-to-end
measurements because they reflect the actual usage and provide a much
stronger signal regarding whether students have good-enough access to
learning resources.

**Single-connection preference.** Modern web traffic uses HTTP/2 and
HTTP/3, multiplexing streams over a single transport connection per origin.
Multi-connection tests inflate numbers in a way no real application does.
Single-connection tests are more representative of the bottleneck that
shapes user experience and the same holds for TLS. You access content
using TLS.

**Satellite RTT is signal, not noise.** High and variable RTT on LEO
links (e.g., Starlink in Malawi, \~110ms median with spikes) is a
real characteristic of the connection that affects every application.
Normalizing it away would hide a condition that students actually
experience. For equatorial deployments, weather-related degradation
(e.g., rain fade) may significantly affect satellite link quality;
cross-correlating measurement results with weather data could help
explain degradation patterns. Similarly, LEO-specific dynamics (beam
sharing, orbital handoffs, variable users per cell) introduce bandwidth
variability beyond what RTT alone captures. Correlating both effects
is out of scope but worth noting given the Malawi use case. That said,
there is a legitimate relative question: given that a connection is
LEO, how good is it compared to what LEO can deliver? This framing
is useful for comparing deployments within the same medium, while the
absolute framing is useful for assessing whether a connection meets
learning-ready thresholds regardless of technology. Both are valid;
they answer different questions. Moreover, with multiple measurement
layers, the normalization question becomes less binary: a LEO connection
might score poorly on raw single-stream throughput but adequately on
the latency-sensitive metrics that matter for specific learning use
cases. Decomposing quality across layers reduces the need to collapse
everything into a single number that then requires normalization. (We
will recompose the signals using IQB-Edu.)

**Medium annotation.** Because Giga manages the Meter client, measurements
can be annotated with metadata about the connection medium (LEO, LEO+WiFi,
ADSL, fiber, mobile with fine-grained classification if possible, e.g.
2G, 3G, LTE, 4G, etc.). This enables per-medium comparisons: how does
this LEO deployment perform relative to other LEO deployments, rather
than only against fiber? For M-Lab's general browser-based measurements,
such annotation is impractical or impossible in general (some ISPs use
distinct ASNs for mobile vs fixed; others share a single ASN across
technologies), but the managed-client model makes it feasible.

Worth noting that Giga Meter uses [https://ipinfo.io/](https://ipinfo.io/)
so any annotation that they apply to internet address blocks could also
be added to our measurements for free.

**Wi-Fi may be part of the measured path.** In some deployments, Giga
Meter connects over Wi-Fi; in others, the device may be wired. When Wi-Fi
is present, it becomes part of the end-to-end measurement (affected by
interference, distance from AP, and humidity), which is consistent with
the end-to-end philosophy. For diagnostic decomposition, Giga Meter
since v2.0.2 collects Wi-Fi link metadata from the OS (signal strength,
link speed, etc.) alongside the network measurements when a wireless
connection is detected. Giga Meter currently runs on Windows, where
this information is available via the Native Wifi API. OONI also collects
information about the kind of access link being used.

**Contention is a scheduling concern.** Measurements run from a single
Giga Meter device. If they run during school hours while students are
active, they naturally capture contended network conditions. If they run
off-hours, they reflect uncontended capacity. Both are useful: a daily
MSAK multi-stream test during off-peak hours could establish maximum
available capacity, while lighter probes during school hours capture
the experience under real load. (However, satellite connectivity uses
electromagnetism, so, yeah, a broken clock...)

**Measurement cost model.** Starlink may be flat-rate, but other deployments
may use metered connectivity. The measurement profile should account for
this: on metered connections, it makes sense to favour lightweight layers
(1-3) and reduce the frequency of bandwidth-heavy tests (layers 4, 5,
7\) to avoid being wasteful.

**Collect multiple layers in a single pass.** Layers 1 through 3 are
lightweight enough that they can be measured within the same session,
reducing overhead and providing a correlated snapshot. (This is an
optimization problem that it is premature to tackle now.)

## Prototype

See [bassosimone/sonda](https://github.com/bassosimone/sonda) for code
that implements part of this design document.
