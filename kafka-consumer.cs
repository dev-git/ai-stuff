using Confluent.Kafka;
using System;
using System.Threading.Tasks;

public class KafkaConsumer
{
    public static async Task Main(string[] args)
    {
        string bootstrapServers = "your_bootstrap_servers"; // Replace with your Kafka broker addresses
        string groupId = "your_group_id"; // Replace with your consumer group ID
        string topicName = "your_topic_name"; // Replace with the topic you want to consume from

        var config = new ConsumerConfig
        {
            BootstrapServers = bootstrapServers,
            GroupId = groupId,
            AutoOffsetReset = AutoOffsetReset.Earliest // Or other desired offset reset strategy
        };

        using (var consumer = new ConsumerBuilder<Ignore, string>(config).Build())
        {
            consumer.Subscribe(topicName);

            try
            {
                while (true)
                {
                    var consumeResult = consumer.Consume(TimeSpan.FromSeconds(10)); // Adjust timeout as needed

                    if (consumeResult != null)
                    {
                        Console.WriteLine($"Received message: Key = {consumeResult.Message.Key}, Value = {consumeResult.Message.Value}");
                        // Process the received message here
                    }
                }
            }
            catch (OperationCanceledException)
            {
                Console.WriteLine("Consumer stopped.");
            }
            finally
            {
                consumer.Close();
            }
        }
    }
}
