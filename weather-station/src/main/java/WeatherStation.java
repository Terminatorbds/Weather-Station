import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.serialization.StringSerializer;

import java.util.Properties;
import java.util.Random;

public class WeatherStation {

    private static final String TOPIC = "weather-readings";
    private static final String[] BATTERY_LEVELS = {"low", "medium", "high"};
    // weighted: low=30%, medium=40%, high=30%
    private static final double[] BATTERY_THRESHOLDS = {0.30, 0.70, 1.00};

    private final long stationId;
    private long seqNo = 0;
    private final Random rng = new Random();

    public WeatherStation(long stationId) {
        this.stationId = stationId;
    }

    private String batteryStatus() {
        double r = rng.nextDouble();
        if (r < BATTERY_THRESHOLDS[0]) return BATTERY_LEVELS[0];
        if (r < BATTERY_THRESHOLDS[1]) return BATTERY_LEVELS[1];
        return BATTERY_LEVELS[2];
    }

    private String buildMessage() {
        int humidity    = rng.nextInt(101);
        int temperature = 32 + rng.nextInt(89);   // 32-120 F
        int windSpeed   = rng.nextInt(101);        // 0-100 km/h
        long ts         = System.currentTimeMillis() / 1000L;

        return "{"
            + "\"station_id\":" + stationId + ","
            + "\"s_no\":" + seqNo + ","
            + "\"battery_status\":\"" + batteryStatus() + "\","
            + "\"status_timestamp\":" + ts + ","
            + "\"weather\":{"
            +   "\"humidity\":" + humidity + ","
            +   "\"temperature\":" + temperature + ","
            +   "\"wind_speed\":" + windSpeed
            + "}}";
    }

    public void run(KafkaProducer<String, String> producer) throws InterruptedException {
        System.out.println("[Station " + stationId + "] Starting...");
        while (true) {
            ++seqNo;  // always increment so receiver can detect gaps
            if (rng.nextDouble() >= 0.10) {
                String json = buildMessage();
                producer.send(new ProducerRecord<>(TOPIC, String.valueOf(stationId), json));
                System.out.println("[Station " + stationId + "] Sent s_no=" + seqNo);
            } else {
                System.out.println("[Station " + stationId + "] Dropped s_no=" + seqNo);
            }
            Thread.sleep(1000);
        }
    }

    public static void main(String[] args) throws InterruptedException {
        String stationIdEnv = System.getenv("STATION_ID");
        long stationId = (stationIdEnv != null) ? Long.parseLong(stationIdEnv) : 1L;

        String bootstrapServers = System.getenv().getOrDefault("BOOTSTRAP_SERVERS", "kafka:9092");

        Properties props = new Properties();
        props.setProperty(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        props.setProperty(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        props.setProperty(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        props.setProperty(ProducerConfig.ACKS_CONFIG, "1");
        props.setProperty(ProducerConfig.RETRIES_CONFIG, "3");

        // Wait for Kafka to be ready
        Thread.sleep(15000);

        try (KafkaProducer<String, String> producer = new KafkaProducer<>(props)) {
            new WeatherStation(stationId).run(producer);
        }
    }
}
