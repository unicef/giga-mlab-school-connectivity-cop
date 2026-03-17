# Research agenda: Measuring school connectivity 

* Version: 1  
* First shared: 2026-03-13  


## Workstream 1: Improving measurement tools

**Task 1.1**: Suggest design for next version Internet measurements that can be incorporated into GigaMeter or other school connectivity measurement tools.   
New measurements, methods and tools can include: application layer measurements (http, QUIC, etc.), measurements to key online services for schools, video streaming (e.g., M-Lab’s neubot experiment for DASH), DNS, etc. The goal is that measurements better capture key performance aspects and contribute to the next version of IQB-Edu. Related to findings from Tasks 1.2 and 2.2.

**Task 1.2** Improve data quality in GigaMeter measurements.

* *Task 1.2.a:* Filter out incorrect measurement and outliers, based on TCP-related information and M-Lab recommended practices (e.g., interrupted tests, unfinished tests, etc.)  
* *Task 1.2.b:* Analyze outlier measurements from existing GigaMeter measurements, identify main patterns, and create filters for measurements pipeline.  
* *Task 1.2.c:* Analyze traceroutes (of GigaMeter measurements) information to filter data in GigaMeter statistics calculations (see also Task 2.1)

**Task 1.3**: Deployment of new M-Lab servers at key locations for school connectivity. The goal is to analyze where we need to / can deploy new M-Lab servers so that (i) the data quality of GigaMeter measurements is improved, (ii) coverage of GigaMeter is extended. Use findings from Tasks 2.3 and 4.2.

## Workstream 2: Characterization of facility-based connectivity

**Task 2.1**: Analyze traceroutes (of GigaMeter measurements) information to filter data in GigaMeter statistics calculations

* Analysis of per school-server traceroutes vs. measurement results. Identify potential outliers and/or non-representative measurements for characterizing performance  
* Based on findings, create filters from traceroutes to filter out measurements that should not be aggregated when calculating performance.

**Task 2.2**: Use traceroutes (of GigaMeter measurements) information to map school connectivity “ecosystem”

* Create a rich dataset per school, with information about its connectivity to the outside world (from/to as many destinations as possible). Include all measurement from all M-Lab servers –even servers far away– to increase diversity of paths.  
* Create an AS-graph (and/or IP-graph) per school from the traceroute information. External datasets can be used to annotate ASNs (e.g., CDNs vs ISPs, tier of top ISPs, IXP presence, etc.). Calculate IP-hop and AS-hop distance and latency of schools to M-Lab servers, main CDNs, IXPs, etc. Identify the number of upstreams and reliability of connections.

**Task 2.3**: Use traceroutes (`IST` measurements) to assess M-Lab measurements fit for school connecting; e.g., while planning new GigaMeter deployments

_Note_: IST: Crowdsourced measurements from users running speed tests through Google Search. IST sees more than 4 million measurements per day.

* Use IST (i.e., from Google Search users; crowdsourced) measurements to identify pairs of ASNs/cities where connectivity to M-Lab servers is good (e.g., servers in proximity, no bottleneck AS-hops) for measuring school connectivity. Related to findings of Tasks 3.1 and 3.2, and feeding into Task 4.x.

**Task 2.4**: Investigate external datasets to enrich characterization of school connectivity (Task 2.2) and improve data quality (can complement Task 1.2) 

* Reverse traceroute datasets  
* IPRS data

## Workstream 3: IQB-Edu

**Task 3.1**: IQB-Edu framework design and scoping (from users to facility).  
Initial design of the variation of the IQB framework and pilot application to Moldova schools. 

* Analyze Moldova school data (non-measurements), for scoping and design  
* Analyze Moldova school GigaMeter measurements, to feed design choices.  
* Apply IQB to Moldova GigaMeter measurements. Design a data aggregation method.

**Task 3.2**: IQB-Edu methodological design \- version 1 (based on findings from Task 3.1).

* Exploratory analysis of parameters for Thresholds and Use cases  
* Sensitivity analysis to data from schools. Moldova and in general.  
* Consider other frameworks, such as, QoO framework, or Brazilian school networks study

**Task 3.3**: Design survey and prototype for feedback from CoP and/or school administrators for the design of IQB-Edu v1 and next design.

## Workstream 4: New insights from existing measurement data

**Task 4.1:** Develop diagnostics based on NDT7 data (e.g., timeseries, anomaly detection). Explore what else (other than current use, or IQB) do measurements can tell us about school connection quality and performance. Identify what other (already collected) metrics are interesting for school connectivity.

**Task 4.2**: Analyze and characterize the impact by deploying GigaMeter in schools. Approximate performance for schools could be obtained by IST (Google Search users / crowdsourced) measurements. Analyze GigaMeter vs IST measurements per country/city/ASN. Identify cases where GigaMeter brings significant value to our understanding of school connectivity by providing more accurate measurements and/or measurements in cases of lack of IST measurements.

## Workstream 5: Open topic \- BYOI (Bring Your Own Ideas)

**Task 5.1**: Organize a hackathon sync or async, online or physical, to collect ideas from the CoP and measurement experts about (i) more research questions, (ii) other information in the M-Lab \<\> Giga dataset that could be useful for other purposes (non related to school connectivity)
