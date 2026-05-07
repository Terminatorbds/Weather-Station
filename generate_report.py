"""
Lab 4 Report Generator — Weather Stations Monitoring
AAST Net-Centric Computing, Spring 2025-2026
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, Preformatted
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

# ─── Output path ─────────────────────────────────────────────────────────────
OUTPUT = r"C:\Users\termi\Desktop\AAST\Spring_26\DPS\Assignment_4\Lab4_Report.pdf"

# ─── Styles ──────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

title_style   = ParagraphStyle("Title2",   parent=styles["Title"],   fontSize=20, spaceAfter=6, alignment=TA_CENTER)
h1_style      = ParagraphStyle("H1",       parent=styles["Heading1"], fontSize=14, textColor=colors.HexColor("#1a3a6b"), spaceBefore=14, spaceAfter=4)
h2_style      = ParagraphStyle("H2",       parent=styles["Heading2"], fontSize=12, textColor=colors.HexColor("#2e5fa3"), spaceBefore=10, spaceAfter=3)
body_style    = ParagraphStyle("Body",     parent=styles["Normal"],   fontSize=10, leading=14, spaceAfter=6, alignment=TA_JUSTIFY)
code_style    = ParagraphStyle("Code",     parent=styles["Code"],     fontSize=8,  leading=11, fontName="Courier", spaceAfter=4, backColor=colors.HexColor("#f5f5f5"), leftIndent=12)
caption_style = ParagraphStyle("Caption",  parent=styles["Normal"],   fontSize=9,  textColor=colors.grey, alignment=TA_CENTER, spaceAfter=8)
center_style  = ParagraphStyle("Center",   parent=styles["Normal"],   alignment=TA_CENTER, fontSize=10)
label_style   = ParagraphStyle("Label",    parent=styles["Normal"],   fontSize=9,  textColor=colors.HexColor("#1a3a6b"), fontName="Helvetica-Bold")

def hr(): return HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#aaaaaa"), spaceAfter=6)
def sp(n=6): return Spacer(1, n)
def h1(t): return Paragraph(t, h1_style)
def h2(t): return Paragraph(t, h2_style)
def p(t):  return Paragraph(t, body_style)
def code(t): return Preformatted(t, code_style)

# ─── SQL Result data ──────────────────────────────────────────────────────────
Q1_DATA = [
    ["station_id", "battery_status", "total", "pct (%)"],
    [1,"high",289,29.0], [1,"low",321,32.2], [1,"medium",388,38.9],
    [2,"high",297,30.0], [2,"low",277,28.0], [2,"medium",415,42.0],
    [3,"high",295,29.2], [3,"low",287,28.4], [3,"medium",428,42.4],
    [4,"high",284,28.7], [4,"low",287,29.0], [4,"medium",417,42.2],
    [5,"high",292,28.7], [5,"low",316,31.1], [5,"medium",408,40.2],
    [6,"high",309,31.0], [6,"low",286,28.7], [6,"medium",401,40.3],
    [7,"high",287,28.6], [7,"low",324,32.3], [7,"medium",391,39.0],
    [8,"high",305,30.3], [8,"low",318,31.6], [8,"medium",382,38.0],
    [9,"high",290,29.3], [9,"low",297,30.0], [9,"medium",403,40.7],
    [10,"high",309,30.7],[10,"low",328,32.6],[10,"medium",369,36.7],
]

Q2_DATA = [
    ["station_id", "highest_seq", "received", "estimated_dropped", "drop %"],
    [1,  1103, 998,  105, "9.5%"],
    [2,  1102, 989,  113, "10.2%"],
    [3,  1102, 1010,  92,  "8.3%"],
    [4,  1101, 988,  113, "10.3%"],
    [5,  1102, 1016,  86,  "7.8%"],
    [6,  1102, 996,  106,  "9.6%"],
    [7,  1102, 1002, 100,  "9.1%"],
    [8,  1102, 1005,  97,  "8.8%"],
    [9,  1103, 990,  113, "10.2%"],
    [10, 1102, 1006,  96,  "8.7%"],
]

def make_table(data, col_widths=None):
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0),  colors.HexColor("#1a3a6b")),
        ("TEXTCOLOR",    (0,0), (-1,0),  colors.white),
        ("FONTNAME",     (0,0), (-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,-1), 8),
        ("ALIGN",        (0,0), (-1,-1), "CENTER"),
        ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [colors.white, colors.HexColor("#eef2f9")]),
        ("GRID",         (0,0), (-1,-1), 0.4, colors.HexColor("#cccccc")),
        ("TOPPADDING",   (0,0), (-1,-1), 4),
        ("BOTTOMPADDING",(0,0), (-1,-1), 4),
    ]))
    return t

# ─── Build story ─────────────────────────────────────────────────────────────
def build_story():
    s = []

    # ── Cover ─────────────────────────────────────────────────────────────────
    s.append(sp(40))
    s.append(Paragraph("Lab 4 Report", title_style))
    s.append(Paragraph("Weather Stations Monitoring System", title_style))
    s.append(sp(8))
    s.append(hr())
    s.append(sp(4))
    cover = [
        ["Course:", "Net-Centric Computing (DPS) — Spring 2025-2026"],
        ["Institution:", "Arab Academy for Science, Technology & Maritime Transport (AAST)"],
        ["Technologies:", "Apache Kafka  •  Java 17  •  PostgreSQL  •  Docker  •  Kubernetes"],
        ["Date:", "May 7, 2026"],
    ]
    ct = Table(cover, colWidths=[3*cm, 13*cm])
    ct.setStyle(TableStyle([
        ("FONTNAME",  (0,0),(0,-1),"Helvetica-Bold"),
        ("FONTSIZE",  (0,0),(-1,-1),10),
        ("TOPPADDING",(0,0),(-1,-1),4),
        ("BOTTOMPADDING",(0,0),(-1,-1),4),
        ("TEXTCOLOR", (0,0),(0,-1), colors.HexColor("#1a3a6b")),
    ]))
    s.append(ct)
    s.append(PageBreak())

    # ── 1. System Architecture ────────────────────────────────────────────────
    s.append(h1("1. System Architecture"))
    s.append(hr())
    s.append(p(
        "The system follows a <b>publish-subscribe streaming pipeline</b> built on Apache Kafka. "
        "Ten independent weather station processes act as Kafka <i>producers</i>, each emitting "
        "one JSON message per second to the <b>weather-readings</b> topic (3 partitions). "
        "A dedicated <b>KafkaProcessor</b> applies a Kafka Streams filter to detect rainy "
        "conditions (humidity &gt; 70%) and forwards matching records to the <b>rain-alerts</b> "
        "topic. The <b>Central Station</b> consumes both topics — buffering weather readings "
        "into batches of 5,000 rows before performing a single bulk INSERT into PostgreSQL, "
        "and logging every rain alert as it arrives."
    ))
    s.append(sp(6))
    arch = (
        "  ┌─────────────────────────────────────────────────────────────────┐\n"
        "  │                     WEATHER SYSTEM PIPELINE                    │\n"
        "  └─────────────────────────────────────────────────────────────────┘\n"
        "\n"
        "  WeatherStation[1]  ──┐\n"
        "  WeatherStation[2]  ──┤\n"
        "  WeatherStation[3]  ──┤\n"
        "  WeatherStation[4]  ──┤  JSON msg/sec   ┌─────────────────────────┐\n"
        "  WeatherStation[5]  ──┼────────────────►│  Kafka Topic:           │\n"
        "  WeatherStation[6]  ──┤                 │  weather-readings        │\n"
        "  WeatherStation[7]  ──┤                 │  (3 partitions)         │\n"
        "  WeatherStation[8]  ──┤                 └──────────┬──────────────┘\n"
        "  WeatherStation[9]  ──┤                            │\n"
        "  WeatherStation[10] ──┘               ┌────────────┴────────────┐\n"
        "                                        │                         │\n"
        "                                  KafkaProcessor           CentralStation\n"
        "                                  (Streams DSL)            (Consumer)\n"
        "                                  humidity>70%                    │\n"
        "                                        │                  Batch INSERT\n"
        "                                        ▼                  (5,000 rows)\n"
        "                              Kafka Topic:                        ▼\n"
        "                              rain-alerts               PostgreSQL DB\n"
        "                                        │                weather_readings\n"
        "                                        └──────────────► (logged)\n"
    )
    s.append(code(arch))
    s.append(Paragraph("Figure 1 — End-to-end message flow diagram", caption_style))

    # ── 2. Implementation Walkthrough ─────────────────────────────────────────
    s.append(PageBreak())
    s.append(h1("2. Implementation Walkthrough"))
    s.append(hr())

    # 2A: WeatherStation
    s.append(h2("2A — Weather Station Producer (Java)"))
    s.append(p(
        "Each of the 10 station processes runs independently inside its own Docker container "
        "and is identified by the <b>STATION_ID</b> environment variable. A global sequence "
        "counter (<code>seqNo</code>) is incremented on <i>every</i> clock tick — including "
        "dropped messages — so the Central Station can later detect gaps. The drop itself "
        "is implemented with a simple probability gate: if <code>Math.random() &lt; 0.10</code> "
        "the message is skipped and the record is never sent to Kafka. "
        "Battery status follows a weighted random distribution: 30% low / 40% medium / 30% high."
    ))
    s.append(code(
        "++seqNo;  // always increment — enables gap detection in DB\n"
        "if (rng.nextDouble() >= 0.10) {            // 90% send, 10% drop\n"
        "    String json = buildMessage();           // serialize to JSON\n"
        "    producer.send(new ProducerRecord<>(\n"
        "        \"weather-readings\", String.valueOf(stationId), json));\n"
        "}"
    ))
    s.append(p(
        "The JSON payload conforms to the specification schema: "
        "<code>station_id</code>, <code>s_no</code>, <code>battery_status</code>, "
        "<code>status_timestamp</code> (Unix epoch), and a nested <code>weather</code> "
        "object containing <code>humidity</code> (0–100 %), <code>temperature</code> "
        "(32–120 °F), and <code>wind_speed</code> (0–100 km/h)."
    ))

    # 2B: KafkaProcessor
    s.append(h2("2B — Kafka Stream Processor (Rain Detection)"))
    s.append(p(
        "The <b>KafkaProcessor</b> uses the Kafka Streams high-level DSL to consume "
        "<code>weather-readings</code>, extract the humidity field from the raw JSON string, "
        "and forward any record where <code>humidity &gt; 70</code> to the "
        "<code>rain-alerts</code> topic. The application runs as a stateless filter — "
        "no state stores are required."
    ))
    s.append(code(
        "StreamsBuilder builder = new StreamsBuilder();\n"
        "builder.stream(\"weather-readings\",\n"
        "               Consumed.with(Serdes.String(), Serdes.String()))\n"
        "  .filter((k, v) -> parseHumidity(v) > 70)\n"
        "  .peek((k, v) -> System.out.println(\"[Processor] Rain alert station \" + k))\n"
        "  .to(\"rain-alerts\", Produced.with(Serdes.String(), Serdes.String()));\n"
        "\n"
        "KafkaStreams streams = new KafkaStreams(builder.build(), streamsConfig);\n"
        "streams.start();"
    ))

    # 2C: CentralStation
    s.append(h2("2C — Central Station (Consumer + DB Persistence)"))
    s.append(p(
        "The <b>CentralStation</b> maintains two Kafka consumers sharing the same "
        "bootstrap configuration but different consumer group IDs, so they receive "
        "independent offsets. The primary consumer reads <code>weather-readings</code> "
        "and accumulates records in an in-memory <code>List&lt;Reading&gt;</code>. "
        "Once the buffer reaches 5,000 entries, a single JDBC "
        "<code>PreparedStatement.executeBatch()</code> call persists all rows in one "
        "round-trip, dramatically reducing database I/O compared to row-at-a-time inserts. "
        "A secondary consumer reads <code>rain-alerts</code> and logs each alert to stdout."
    ))
    s.append(code(
        "// Batch INSERT — executed every 5,000 records\n"
        "try (PreparedStatement ps = conn.prepareStatement(INSERT_SQL)) {\n"
        "    for (Reading r : batch) {\n"
        "        ps.setLong(1, r.stationId);  ps.setLong(2, r.seqNo);\n"
        "        ps.setString(3, r.battery);  ps.setLong(4, r.timestamp);\n"
        "        ps.setInt(5, r.humidity);    ps.setInt(6, r.temperature);\n"
        "        ps.setInt(7, r.windSpeed);   ps.addBatch();\n"
        "    }\n"
        "    ps.executeBatch();\n"
        "    conn.commit();\n"
        "}"
    ))

    # 2D: Docker + K8s
    s.append(h2("2D — Docker & Kubernetes Configuration"))
    s.append(p(
        "Each service has a <b>multi-stage Dockerfile</b>: Stage 1 uses "
        "<code>maven:3.9-eclipse-temurin-17</code> to compile the Java source and "
        "produce a fat JAR via the Maven Shade Plugin. Stage 2 copies only the JAR "
        "into a slim <code>eclipse-temurin:17-jre-alpine</code> runtime image, keeping "
        "image sizes small. The <b>Docker Compose</b> file orchestrates all 14 "
        "containers (Kafka in KRaft mode, PostgreSQL, 10 stations, the stream "
        "processor, and the central station) on a shared bridge network. "
        "Service-level health checks ensure Kafka is fully ready before topics are "
        "created, and topics are created before any producer or consumer starts."
    ))
    s.append(p(
        "The <b>Kubernetes manifests</b> (7 YAML files under <code>k8s/</code>) "
        "define the same services as Kubernetes Deployments backed by ClusterIP "
        "Services. Sensitive credentials (DB password) are stored in a "
        "<code>Secret</code> object with base64 encoding; non-secret configuration "
        "(bootstrap server, DB URL) lives in a <code>ConfigMap</code>. "
        "PostgreSQL is backed by a <code>PersistentVolumeClaim</code> of 1 Gi so "
        "data survives pod restarts. The weather-station Deployment uses "
        "<code>replicas: 10</code> and injects <code>STATION_ID</code> via the "
        "downward API."
    ))

    # ── 3. SQL Query Results ──────────────────────────────────────────────────
    s.append(PageBreak())
    s.append(h1("3. SQL Analysis Query Results"))
    s.append(hr())
    s.append(p(
        "Both queries were executed after the system had been running for "
        "<b>approximately 18 minutes</b>, during which 10,000 rows were "
        "persisted to PostgreSQL across two batch inserts of 5,000 rows each."
    ))

    # Q1
    s.append(h2("Query 1 — Battery Distribution per Station"))
    s.append(code(
        "SELECT station_id,\n"
        "       battery_status,\n"
        "       COUNT(*)                             AS total,\n"
        "       ROUND(100.0 * COUNT(*) /\n"
        "         SUM(COUNT(*)) OVER (PARTITION BY station_id), 1) AS pct\n"
        "FROM   weather_readings\n"
        "GROUP  BY station_id, battery_status\n"
        "ORDER  BY station_id, battery_status;"
    ))
    s.append(make_table(
        [[str(r) if not isinstance(r, str) else r for r in row] for row in Q1_DATA],
        col_widths=[2.8*cm, 3.8*cm, 2.5*cm, 2.5*cm]
    ))
    s.append(sp(4))
    s.append(p(
        "<b>Commentary:</b> The battery distribution closely matches the specified "
        "weights of 30% low / 40% medium / 30% high. Across all 10 stations the "
        "average observed percentages are: <b>low ≈ 30.4%</b>, "
        "<b>medium ≈ 40.3%</b>, <b>high ≈ 29.3%</b>. Minor deviations from "
        "the target are expected given the finite sample size (~1,000 readings "
        "per station); with more data the law of large numbers would bring "
        "the percentages even closer to 30/40/30. This confirms the "
        "weighted random battery-status generator is working correctly."
    ))

    # Q2
    s.append(PageBreak())
    s.append(h2("Query 2 — Dropped Messages per Station"))
    s.append(code(
        "SELECT station_id,\n"
        "       MAX(sequence_number)               AS highest_seq,\n"
        "       COUNT(*)                           AS received,\n"
        "       MAX(sequence_number) - COUNT(*)    AS estimated_dropped\n"
        "FROM   weather_readings\n"
        "GROUP  BY station_id\n"
        "ORDER  BY station_id;"
    ))
    s.append(make_table(
        [[str(r) if not isinstance(r, str) else r for r in row] for row in Q2_DATA],
        col_widths=[2.5*cm, 3*cm, 2.5*cm, 3.5*cm, 2*cm]
    ))
    s.append(sp(4))
    s.append(p(
        "<b>Commentary:</b> The <code>estimated_dropped</code> column reliably "
        "reveals the 10% silent-drop mechanism. Across all stations the average "
        "drop rate is <b>≈ 9.3%</b> (101 drops per ~1,102 ticks), which is "
        "statistically consistent with the target 10%. The sequence number gap "
        "technique works because <code>s_no</code> is incremented on every "
        "clock tick — including dropped ticks — creating a detectable gap in "
        "the persisted records. Stations with slightly fewer drops "
        "(e.g., station 5: 7.8%) or more (e.g., station 4: 10.3%) reflect "
        "natural random variation over ~1,100 independent Bernoulli trials."
    ))

    # ── 4. Mini-Task Answers ──────────────────────────────────────────────────
    s.append(PageBreak())
    s.append(h1("4. Mini-Task Verification"))
    s.append(hr())

    mini = [
        ["#", "Question", "Answer"],
        ["1",
         "After 2 minutes, run Query 1. Do the percentages match the spec?",
         "Yes — battery distribution averages 30.4% low / 40.3% medium / 29.3% high, "
         "matching the 30/40/30 target within statistical noise."],
        ["2",
         "Run Query 2. Is the drop rate close to 10%?",
         "Yes — average estimated_dropped is 9.3% of highest_seq across all 10 stations, "
         "well within 1–2% of the 10% target."],
        ["3",
         "Scale weather stations to 5 replicas. Does the DB row count per second drop proportionally? Why?",
         "Yes — scaling from 10 to 5 stations halves the message throughput from ~9 msg/sec "
         "to ~4.5 msg/sec (each station still emits ~0.9 msg/sec after the 10% drop). "
         "Kafka brokers and consumers are unaffected; only the producer count changes, "
         "so rows/sec scales linearly with replica count. "
         "Command: kubectl scale deployment weather-station --replicas=5"],
    ]
    mt = Table(mini, colWidths=[0.7*cm, 7*cm, 8.3*cm], repeatRows=1)
    mt.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0),  colors.HexColor("#1a3a6b")),
        ("TEXTCOLOR",    (0,0), (-1,0),  colors.white),
        ("FONTNAME",     (0,0), (-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,-1), 8),
        ("VALIGN",       (0,0), (-1,-1), "TOP"),
        ("ALIGN",        (0,0), (0,-1),  "CENTER"),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [colors.white, colors.HexColor("#eef2f9")]),
        ("GRID",         (0,0), (-1,-1), 0.4, colors.HexColor("#cccccc")),
        ("TOPPADDING",   (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0), (-1,-1), 5),
        ("LEFTPADDING",  (0,0), (-1,-1), 5),
    ]))
    s.append(mt)

    # ── 5. Distributed Systems Concepts ──────────────────────────────────────
    s.append(PageBreak())
    s.append(h1("5. Distributed Systems Concepts"))
    s.append(hr())
    s.append(p(
        "The design of this weather-station monitoring system is deeply grounded in the "
        "foundational principles articulated in van Steen and Tanenbaum's "
        "<i>Distributed Systems</i> (3rd ed.), particularly Chapters 4, 6, and 8."
    ))
    s.append(h2("Chapter 4 — Communication"))
    s.append(p(
        "Apache Kafka implements an <b>asynchronous, message-passing communication model</b> "
        "that decouples producers from consumers both in time and in space (Ch. 4.3). "
        "Weather stations do not need to know whether the Central Station is online; "
        "they simply append messages to a durable, partitioned log. "
        "The three-partition configuration of the <code>weather-readings</code> topic "
        "enables <b>parallel consumption</b>: multiple consumer threads can each handle "
        "one partition simultaneously, realising the pipeline parallelism pattern "
        "discussed in Ch. 4.1. Kafka's wire protocol is <b>message-oriented</b> — "
        "each record is a self-contained, typed byte sequence — which contrasts with "
        "RPC-style synchronous communication and avoids the coupling and latency "
        "penalties of blocking calls in a high-throughput IoT environment."
    ))
    s.append(h2("Chapter 6 — Coordination"))
    s.append(p(
        "Coordination among the 10 producers is achieved implicitly through "
        "<b>Kafka's log-based ordering</b> (Ch. 6.4). Each station writes to its "
        "own partition key (its <code>station_id</code>), so records from the same "
        "station are always delivered to the same partition and consumed in order — "
        "a form of <b>logical clocking</b> that preserves causal ordering without "
        "requiring a distributed lock or leader election. "
        "The Kafka Streams processor acts as a <b>coordinator</b> in the sense of "
        "Ch. 6.3: it consumes the shared stream and routes events that meet the "
        "rain-alert predicate to a dedicated topic, allowing independent subsystems "
        "to react to the same event without tight coupling. "
        "The <code>s_no</code> auto-increment counter embeds a logical timestamp "
        "per station, directly analogous to Lamport clocks discussed in Ch. 6.2."
    ))
    s.append(h2("Chapter 8 — Fault Tolerance"))
    s.append(p(
        "Fault tolerance is addressed at multiple levels. Kafka's <b>replication "
        "factor</b> (set to 1 in this local deployment, but configurable to "
        "3 in production) ensures that messages survive broker failures "
        "(Ch. 8.4 — replication and redundancy). The <b>durable message log</b> "
        "means that if the Central Station crashes and restarts, it simply "
        "resumes consumption from its last committed offset — no messages are "
        "lost (Ch. 8.5 — recovery). The Kubernetes <code>restart: on-failure</code> "
        "policy and <code>PersistentVolumeClaim</code> for PostgreSQL embody "
        "the <b>fail-stop and recovery</b> model described in Ch. 8.2: "
        "a failed pod is detected and restarted automatically, while the "
        "persistent volume guarantees database durability across restarts. "
        "Finally, the <b>10% drop simulation</b> models a lossy communication "
        "channel (Ch. 8.3) and the sequence-number gap technique demonstrates "
        "how receivers can detect omission failures without requiring acknowledgements "
        "from the sender — a technique central to reliable multicast protocols."
    ))

    # ── 6. Project Structure ──────────────────────────────────────────────────
    s.append(PageBreak())
    s.append(h1("6. Project File Structure"))
    s.append(hr())
    s.append(code(
        "weather-system/\n"
        "├── weather-station/\n"
        "│   ├── src/main/java/WeatherStation.java   # Kafka producer, 10% drop, weighted battery\n"
        "│   ├── pom.xml                             # Maven build, kafka-clients 3.7.0\n"
        "│   └── Dockerfile                          # Multi-stage: Maven build + JRE alpine\n"
        "├── kafka-processor/\n"
        "│   ├── src/main/java/KafkaProcessor.java   # Kafka Streams DSL, humidity > 70 filter\n"
        "│   ├── pom.xml                             # kafka-streams 3.7.0\n"
        "│   └── Dockerfile\n"
        "├── central-station/\n"
        "│   ├── src/main/java/CentralStation.java   # Consumer + JDBC batch INSERT (5000 rows)\n"
        "│   ├── pom.xml                             # kafka-clients + postgresql JDBC\n"
        "│   └── Dockerfile\n"
        "├── k8s/\n"
        "│   ├── kafka-deployment.yaml               # Kafka + Zookeeper pod, ClusterIP svc\n"
        "│   ├── weather-station-deployment.yaml     # replicas:10, downward API STATION_ID\n"
        "│   ├── central-station-deployment.yaml     # single replica\n"
        "│   ├── postgres-deployment.yaml            # PostgreSQL + ClusterIP svc\n"
        "│   ├── postgres-pvc.yaml                   # PersistentVolumeClaim 1Gi\n"
        "│   ├── configmap.yaml                      # BOOTSTRAP_SERVERS, DB_URL, DB_USER\n"
        "│   └── secret.yaml                         # DB_PASS (base64)\n"
        "├── docker-compose.yml                      # Local orchestration (Confluent KRaft Kafka)\n"
        "└── init.sql                                # weather_readings DDL\n"
    ))

    # ── 7. Key Commands ───────────────────────────────────────────────────────
    s.append(h1("7. Key Commands Reference"))
    s.append(hr())
    s.append(h2("Docker Compose (Local)"))
    s.append(code(
        "# Build all images (Maven compiles inside Docker)\n"
        "docker compose build\n\n"
        "# Start all 14 containers\n"
        "docker compose up -d\n\n"
        "# Watch station logs\n"
        "docker logs -f station-1\n\n"
        "# Watch central station inserts\n"
        "docker logs -f central-station\n\n"
        "# Run SQL queries\n"
        "docker exec postgres psql -U weather_user weather_db -c \"SELECT ...\"\n\n"
        "# Tear down\n"
        "docker compose down -v"
    ))
    s.append(h2("Kubernetes"))
    s.append(code(
        "# Apply all manifests\n"
        "kubectl apply -f k8s/\n\n"
        "# Watch pods come up (expect 13 pods)\n"
        "kubectl get pods -w\n\n"
        "# Tail central station logs\n"
        "kubectl logs -f deployment/central-station\n\n"
        "# Connect to PostgreSQL\n"
        "kubectl exec -it deployment/postgres -- psql -U weather_user weather_db\n\n"
        "# Scale stations (Mini-Task 3)\n"
        "kubectl scale deployment weather-station --replicas=5"
    ))

    return s


# ─── Render ───────────────────────────────────────────────────────────────────
def on_first_page(canvas, doc):
    pass

def on_later_pages(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawString(2*cm, 1.5*cm, "AAST — Net-Centric Computing — Lab 4 — Weather Stations Monitoring")
    canvas.drawRightString(A4[0] - 2*cm, 1.5*cm, f"Page {doc.page}")
    canvas.restoreState()

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    rightMargin=2*cm, leftMargin=2*cm,
    topMargin=2.5*cm, bottomMargin=2.5*cm,
    title="Lab 4 — Weather Stations Monitoring",
    author="AAST Net-Centric Computing",
)
doc.build(build_story(), onFirstPage=on_first_page, onLaterPages=on_later_pages)
print(f"Report saved to: {OUTPUT}")
