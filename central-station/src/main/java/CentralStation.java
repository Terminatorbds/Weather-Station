import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.common.serialization.StringDeserializer;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.time.Duration;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Properties;

public class CentralStation {

    private static final String READINGS_TOPIC = "weather-readings";
    private static final String ALERTS_TOPIC   = "rain-alerts";
    private static final int    BATCH_SIZE     = 5000;

    private static final String INSERT_SQL =
        "INSERT INTO weather_readings (station_id, sequence_number, battery_status, timestamp, humidity, temperature, wind_speed) " +
        "VALUES (?, ?, ?, ?, ?, ?, ?)";

    // --- simple JSON field extractors ---
    private static long   parseLong(String json, String key) {
        int idx = json.indexOf("\"" + key + "\":");
        if (idx < 0) return 0;
        int s = idx + key.length() + 3;
        while (s < json.length() && !Character.isDigit(json.charAt(s))) s++;
        int e = s;
        while (e < json.length() && Character.isDigit(json.charAt(e))) e++;
        try { return Long.parseLong(json.substring(s, e)); } catch (Exception ex) { return 0; }
    }

    private static int parseInt(String json, String key) {
        return (int) parseLong(json, key);
    }

    private static String parseString(String json, String key) {
        int idx = json.indexOf("\"" + key + "\":\"");
        if (idx < 0) return "";
        int s = idx + key.length() + 4;
        int e = json.indexOf("\"", s);
        return e < 0 ? "" : json.substring(s, e);
    }

    // --- reading entry ---
    static class Reading {
        long   stationId, seqNo, timestamp;
        String battery;
        int    humidity, temperature, windSpeed;
    }

    private static Reading parse(String json) {
        Reading r = new Reading();
        r.stationId   = parseLong(json, "station_id");
        r.seqNo       = parseLong(json, "s_no");
        r.battery     = parseString(json, "battery_status");
        r.timestamp   = parseLong(json, "status_timestamp");
        r.humidity    = parseInt(json, "humidity");
        r.temperature = parseInt(json, "temperature");
        r.windSpeed   = parseInt(json, "wind_speed");
        return r;
    }

    private static void flushBatch(Connection conn, List<Reading> batch) throws SQLException {
        try (PreparedStatement ps = conn.prepareStatement(INSERT_SQL)) {
            for (Reading r : batch) {
                ps.setLong(1, r.stationId);
                ps.setLong(2, r.seqNo);
                ps.setString(3, r.battery);
                ps.setLong(4, r.timestamp);
                ps.setInt(5, r.humidity);
                ps.setInt(6, r.temperature);
                ps.setInt(7, r.windSpeed);
                ps.addBatch();
            }
            ps.executeBatch();
            conn.commit();
            System.out.println("[Central] Flushed " + batch.size() + " rows to DB");
        }
    }

    public static void main(String[] args) throws Exception {
        String bootstrapServers = System.getenv().getOrDefault("BOOTSTRAP_SERVERS", "kafka:9092");
        String dbUrl  = System.getenv().getOrDefault("DB_URL", "jdbc:postgresql://postgres:5432/weather_db");
        String dbUser = System.getenv().getOrDefault("DB_USER", "weather_user");
        String dbPass = System.getenv().getOrDefault("DB_PASS", "weather_pass");

        // Wait for Kafka and Postgres to be ready
        Thread.sleep(25000);

        // DB connection
        Connection conn = DriverManager.getConnection(dbUrl, dbUser, dbPass);
        conn.setAutoCommit(false);

        // Create table if not exists
        try (java.sql.Statement st = conn.createStatement()) {
            st.execute(
                "CREATE TABLE IF NOT EXISTS weather_readings (" +
                "  id               BIGSERIAL PRIMARY KEY," +
                "  station_id       BIGINT," +
                "  sequence_number  BIGINT," +
                "  battery_status   VARCHAR(10)," +
                "  timestamp        BIGINT," +
                "  humidity         INT," +
                "  temperature      INT," +
                "  wind_speed       INT" +
                ")"
            );
            conn.commit();
        }

        // Consumer for weather-readings
        Properties consumerProps = new Properties();
        consumerProps.setProperty(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        consumerProps.setProperty(ConsumerConfig.GROUP_ID_CONFIG, "central-station-group");
        consumerProps.setProperty(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        consumerProps.setProperty(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        consumerProps.setProperty(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        consumerProps.setProperty(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, "true");

        // Consumer for rain-alerts (separate group for logging)
        Properties alertProps = new Properties();
        alertProps.putAll(consumerProps);
        alertProps.setProperty(ConsumerConfig.GROUP_ID_CONFIG, "rain-alert-logger");

        List<Reading> buffer = new ArrayList<>();
        long totalInserted = 0;

        try (KafkaConsumer<String, String> consumer = new KafkaConsumer<>(consumerProps);
             KafkaConsumer<String, String> alertConsumer = new KafkaConsumer<>(alertProps)) {

            consumer.subscribe(Arrays.asList(READINGS_TOPIC));
            alertConsumer.subscribe(Arrays.asList(ALERTS_TOPIC));

            System.out.println("[Central] Listening on " + READINGS_TOPIC + " and " + ALERTS_TOPIC);

            while (true) {
                // Poll readings
                ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(500));
                for (ConsumerRecord<String, String> record : records) {
                    buffer.add(parse(record.value()));
                    if (buffer.size() >= BATCH_SIZE) {
                        flushBatch(conn, buffer);
                        totalInserted += buffer.size();
                        buffer.clear();
                        System.out.println("[Central] Total rows: " + totalInserted);
                    }
                }

                // Poll alerts (log only, small batch)
                ConsumerRecords<String, String> alerts = alertConsumer.poll(Duration.ofMillis(100));
                for (ConsumerRecord<String, String> alert : alerts) {
                    System.out.println("[Central] RAIN ALERT from station " + alert.key() + ": " + alert.value());
                }

                // Flush partial buffer every 30 seconds worth (avoid infinite wait on small datasets)
                if (!buffer.isEmpty() && buffer.size() % 100 == 0) {
                    System.out.println("[Central] Buffer size: " + buffer.size() + " (waiting for " + BATCH_SIZE + ")");
                }
            }
        }
    }
}
