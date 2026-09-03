namespace OseBe.Contexts.Messaging

open System.Diagnostics.CodeAnalysis
open System.Text
open System.Threading.Tasks
open NATS.Client.Core
open NATS.Client.JetStream
open NATS.Client.JetStream.Models
open OseBe.Contexts.Messaging.Domain

/// Infrastructure adapter for the messaging bounded context: the JetStream
/// durable publish/consume/ack demo proving at-least-once delivery at startup.
module Infrastructure =

    /// JetStream stream name for the demo.
    [<Literal>]
    let StreamName = "OSE_APP_MESSAGING_DEMO"

    /// NATS subject for demo messages.
    [<Literal>]
    let Subject = "ose-app.messaging.demo"

    /// Durable consumer name for the demo.
    [<Literal>]
    let ConsumerName = "ose-app-messaging-demo"

    /// Runs the JetStream durable demo against a connected NATS client: create or
    /// get the stream and durable consumer, publish one demo message, then fetch
    /// and acknowledge it. Returns the outcome.
    [<ExcludeFromCodeCoverage(Justification = "Requires a live NATS JetStream broker; e2e-tested per the @e2e-tagged specs/apps/ose/be/behaviors/messaging/live/jetstream-demo.feature, owned by ose-be-e2e")>]
    let runDemo (conn: NatsConnection) : Task<JetStreamDemoOutcome> =
        task {
            try
                let js = NatsJSContext(conn :> INatsConnection)

                let streamConfig = StreamConfig(name = StreamName, subjects = [| Subject |])
                let! _stream = js.CreateStreamAsync(streamConfig)

                let consumerConfig = ConsumerConfig(ConsumerName)
                let! consumer = js.CreateOrUpdateConsumerAsync(StreamName, consumerConfig)

                let payload = Encoding.UTF8.GetBytes("demo message")
                let! _ack = js.PublishAsync<byte[]>(Subject, payload)

                let opts = NatsJSFetchOpts(MaxMsgs = 1)
                let messages = consumer.FetchAsync<byte[]>(opts)
                let enumerator = messages.GetAsyncEnumerator()
                let mutable acked = false

                let! hasNext = enumerator.MoveNextAsync()

                if hasNext then
                    do! enumerator.Current.AckAsync()
                    acked <- true

                do! enumerator.DisposeAsync()

                if acked then
                    return DeliveredAndAcked
                else
                    return Failed "no message delivered"
            with ex ->
                return Failed ex.Message
        }
