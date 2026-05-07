import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.kstream.Consumed;
import org.apache.kafka.streams.kstream.Produced;

import java.util.Properties;

public class KafkaProcessor {

    private static final String INPUT_TOPIC  = "weather-readings";
    private static final String OUTPUT_TOPIC = "rain-alerts";

    private static int parseHumidity(String json) {
        try {
            int idx = json.indexOf("\"humidity\":");
            if (idx < 0) return 0;
            int start = idx + 11;
            int end = start;
            while (end < json.length() && (Character.isDigit(json.charAt(end)))) end++;
            return Integer.parseInt(json.substring(start, end));
        } catch (Exception e) {
            return 0;
        }
    }

    public static void main(String[] args) throws InterruptedException {
        String bootstrapServers = System.getenv().getOrDefault("BOOTSTRAP_SERVERS", "kafka:9092");

        Properties props = new Properties();
        props.setProperty(StreamsConfig.APPLICATION_ID_CONFIG, "rain-detector");
        props.setProperty(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        props.setProperty(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass().getName());
        props.setProperty(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass().getName());

        // Wait for Kafka to be ready
        Thread.sleep(20000);

        StreamsBuilder builder = new StreamsBuilder();
        builder.stream(INPUT_TOPIC, Consumed.with(Serdes.String(), Serdes.String()))
               .filter((k, v) -> parseHumidity(v) > 70)
               .peek((k, v) -> System.out.println("[Processor] Rain alert station " + k + " humidity=" + parseHumidity(v)))
               .to(OUTPUT_TOPIC, Produced.with(Serdes.String(), Serdes.String()));

        KafkaStreams streams = new KafkaStreams(builder.build(), props);
        Runtime.getRuntime().addShutdownHook(new Thread(streams::close));
        streams.start();

        System.out.println("[Processor] Rain detection stream started");
    }
}
