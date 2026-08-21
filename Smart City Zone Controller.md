# Smart City Zone Controller — Tasks 9–14

## 9. Distributed Architecture and Communication Plan

### Architecture Choice: Client-Server

**Chosen architecture: Client-Server.**

The three zone controllers act as clients, while the central Smart City Operations dashboard/backend acts as the server.

The Client-Server architecture is appropriate for this platform for the following reasons:

- **Transparency:** A central service provides one consistent interface for all three zone controllers. Controllers do not need to know the internal implementation of the dashboard/backend.
- **Scalability:** Additional zone controllers can be added as clients without redesigning the overall communication model. The central backend can also be scaled horizontally.
- **Fault tolerance:** Redundant backend instances, replicated storage, health checks, and local buffering at zone controllers can reduce the impact of component failures.
- **Single point of failure:** A basic Client-Server architecture has a central dependency, so production deployment should use redundant backend instances and failover rather than relying on one physical server.

### (a) Zone controller pushing a real-time public-safety alert

**Communication type: Asynchronous**

**Protocol: MQTT over TLS**

MQTT is suitable because it is lightweight and designed for IoT messaging. The zone controller can publish a public-safety alert without blocking its sensor-processing workload while waiting for the dashboard to respond. The dashboard/backend can subscribe to the relevant alert topic and receive the event immediately.

TLS should be used with MQTT to protect the alert against interception and modification.

### (b) Zone controller uploading its full day's sensor log

**Communication type: Asynchronous**

**Protocol: HTTPS**

The full sensor log is a batch operation and does not need to block real-time sensor processing. The controller can upload the log asynchronously and retry the upload if the archival service is temporarily unavailable.

HTTPS provides reliable and encrypted delivery of the complete sensor log.

---

# 10. VPC-Based Network Boundary

## VPC Design

I would use **one VPC containing three dedicated subnets**:

- `Zone-A-Subnet`
- `Zone-B-Subnet`
- `Zone-C-Subnet`

Each zone controller and its directly associated resources would be placed inside its respective subnet.

A single VPC keeps the overall architecture manageable while the three subnets provide logical separation between Zone-A, Zone-B, and Zone-C.

A VPC provides **logical isolation** from other networks, while its routing tables, security groups/firewalls, subnet configuration, and network access controls provide the **customizability** required to define exactly which traffic is allowed between the zones.

## Network-Level Control

The specific control preventing direct access between zones is a:

**Stateful firewall/security-group rule denying inbound traffic from the CIDR range of other zone subnets.**

For example, Zone-A's security group would not contain an inbound rule allowing traffic from the Zone-B subnet CIDR.

Equivalent isolation rules would be applied to the other zone security groups.

Therefore:

```text
Zone-B-Subnet
     |
     | X  Denied by security-group/firewall rule
     |
Zone-A-Subnet






| Security Objective         | Specific Control / Technology                  | How It Protects the Platform                                                                                                                                                                                  |
| -------------------------- | ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Protect sensitive data** | AES-256 encryption at rest                     | Sensor logs, controller configuration, credentials, and other stored sensitive information are encrypted. If storage is stolen or accessed without authorization, the underlying plaintext data is protected. |
| **Authentication**         | Mutual TLS (mTLS) with device certificates     | Each zone controller must prove its identity using a trusted certificate before the central service accepts its communication. This prevents unauthorized devices from impersonating legitimate controllers.  |
| **Authorization**          | Role-Based Access Control (RBAC)               | Users and services receive permissions based on their assigned roles. This prevents users from performing operations outside their responsibilities.                                                          |
| **Prevent cyber attacks**  | Web Application Firewall (WAF)                 | A WAF can inspect and block malicious application-layer requests, including attacks such as SQL injection and malicious HTTP requests against the dashboard/backend.                                          |
| **Secure communication**   | TLS 1.3                                        | TLS encrypts and integrity-protects information travelling between zone controllers and central services, including public-safety alerts and telemetry.                                                       |
| **Ensure availability**    | Load balancer with redundant backend instances | If one backend instance fails, the load balancer can direct traffic to a healthy instance. This prevents a single server failure from taking the dashboard/backend offline.                                   |






| IAM Role                 | Specific Permission Set                                                                                                                                                                                          |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Zone Operator**        | Read telemetry for the assigned zone, acknowledge public-safety alerts, view controller health, and perform approved operations on the assigned zone controller. No access to other zones or IAM administration. |
| **City Dashboard Admin** | Read telemetry and alerts from all three zones, manage dashboard configuration, view system health, and perform approved dashboard administration. Cannot modify audit records.                                  |
| **Auditor**              | Read-only access to audit logs, security events, configuration history, and compliance reports. Cannot modify jobs, controller configuration, or IAM permissions.                                                |
| **Platform/IAM Admin**   | Manage IAM roles, service identities, security policies, and approved platform configuration. This role is separated from normal zone operations.                                                                |



| Data State     | Protection Technique                                | Concrete Platform Example                                                                                                                                                             |
| -------------- | --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **At Rest**    | AES-256 encryption                                  | The fixed `JOBS` list and archived sensor logs stored on a zone controller or central storage are encrypted so unauthorized access to the storage does not expose the plaintext data. |
| **In Transit** | TLS 1.3                                             | A real-time public-safety alert sent from Zone-B's controller to the central dashboard/backend is encrypted while travelling across the network.                                      |
| **In Use**     | Process isolation and least-privilege memory access | During the Banker's Algorithm safety check, `AVAILABLE`, `MAX_NEED`, `ALLOCATION`, and `Need` are held in application memory and accessed only by the process that requires them.     |




| Sensor / Device                     | Communication Technology | Reason                                                                                                                                                                                                                     |
| ----------------------------------- | ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Traffic-camera trigger/device**   | **5G**                   | Traffic-camera events can require relatively high bandwidth and low latency, especially when transmitting event images or video metadata. 5G provides high throughput and low latency for city-scale deployments.          |
| **Environmental sensor**            | **LoRaWAN**              | Environmental sensors commonly transmit small measurements periodically and may operate on batteries. LoRaWAN provides long range with low power consumption, making it suitable for distributed environmental monitoring. |
| **Wearable public-safety device**   | **Bluetooth**            | A wearable normally communicates over a short distance with a nearby phone or gateway. Bluetooth provides appropriate short-range connectivity with low power consumption.                                                 |
| **Fixed smart-city sensor cluster** | **Zigbee**               | Zigbee provides low-power local communication and supports mesh networking, making it suitable for groups of nearby sensors.                                                                                               |


Six IoT Architecture Layers
1. Physical Environment

This layer represents the real-world environment in which the smart-city platform operates.

Examples include:

Roads
Traffic intersections
Public spaces
Weather conditions
Air quality
Buildings
Public-safety personnel
2. Perception / Device Layer

This layer contains the physical devices that sense or detect events.

Examples include:

Traffic-camera triggers
Environmental sensors
Air-quality sensors
Temperature and humidity sensors
Wearable public-safety devices
Other IoT sensing devices

These devices collect measurements and events from the physical environment.

3. Gateway Layer

The gateway layer contains zone-specific IoT gateways.

The gateways:

Aggregate sensor traffic
Perform protocol conversion when required
Buffer sensor data
Filter or validate incoming events
Forward information toward the zone controller and central platform

For example, a gateway can collect Zigbee or Bluetooth sensor data and forward it using IP-based networking.

4. Network Communication Layer

This layer provides communication between sensors, gateways, zone controllers, and central services.

Technologies include:

Bluetooth
Zigbee
LoRaWAN
5G
IP networking
MQTT
HTTPS
TLS

The network layer transports telemetry, public-safety alerts, logs, and control information.

5. Cloud Platform Layer

Part 1's fixed compute engine is the Cloud Platform Layer.

It contains the fixed compute workload and algorithms developed in Part 1, including:

FCFS
Non-preemptive SJF
SRTF
Round Robin
Priority scheduling
Peterson's Algorithm
Banker's Algorithm
Paging
Segmentation

The engine processes the sensor-processing workload and supports the platform's compute and resource-management functions.

6. Application Layer

The application layer contains the central Smart City Operations dashboard.

It provides authorized city personnel with:

Sensor telemetry
Public-safety alerts
Zone status
Controller health
Processing information
Operational monitoring
Historical data and reports
14. Threats and Mitigations
Threat 1 — IoT Device Spoofing / Unauthorized Device Access

An attacker could attempt to impersonate a legitimate sensor or zone controller and inject false telemetry or fake public-safety alerts.

Mitigation

Use mutual TLS with per-device certificates.

The central service verifies the certificate presented by each device before accepting its data. Compromised device certificates can also be revoked.

Threat 2 — Man-in-the-Middle Attack

An attacker positioned on the communication path could attempt to intercept or modify a public-safety alert sent from a zone controller to the central dashboard.

Mitigation

Use TLS 1.3 with certificate validation.

TLS provides confidentiality and integrity for the communication and allows the communicating endpoints to verify the intended service.

Threat 3 — Denial-of-Service Attack

An attacker could flood the dashboard/backend or IoT-facing services with excessive requests, preventing legitimate zone controllers from delivering alerts and telemetry.

Mitigation

Use a Web Application Firewall, rate limiting, load balancing, and redundant backend instances.

The WAF and rate limiting can filter or restrict abusive traffic, while the load balancer and redundant instances help maintain service availability.

Threat 4 — Vulnerable or Compromised IoT Firmware

An outdated or vulnerable sensor could provide an attacker with an entry point into one of the zone networks.

Mitigation

Require signed firmware updates and regular security patching.

IoT devices should also remain inside their assigned zone subnet so that compromise of one device does not provide unrestricted access to other zones.

Threat 5 — Cloud Credential Compromise

If an administrator's credentials are stolen, an attacker could potentially modify dashboard configuration, access sensitive information, or change platform settings.

Mitigation

Use MFA, RBAC, least privilege, short-lived credentials, and audit logging.

Privileged operations should be logged and monitored so suspicious administrative activity can be detected.

Final Design Summary
Area	Decision
Distributed architecture	Client-Server
Real-time public-safety alert	Asynchronous MQTT over TLS
Daily sensor-log archival	Asynchronous HTTPS
Network boundary	One VPC with three isolated zone subnets
Cross-zone isolation control	Security-group/firewall rules
Sensitive data at rest	AES-256 encryption
Data in transit	TLS 1.3
Data in use	Process isolation and least-privilege memory access
IoT connectivity	5G, LoRaWAN, Bluetooth, Zigbee
Cloud Platform Layer	Part 1's fixed compute engine
Authentication	Mutual TLS/device certificates
Authorization	RBAC
Attack prevention	WAF
Availability	Load balancing + redundant backend instances
Primary IoT threats addressed	Device spoofing, MITM, DoS, vulnerable firmware
Cloud threat addressed	Credential compromise