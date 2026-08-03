# This actor cannot consume while it is doing a long unit of work.
worker = spawn(fn -> Process.sleep(100) end)
for _ <- 1..100, do: send(worker, :work)
Process.sleep(10)
{:message_queue_len, queued} = Process.info(worker, :message_queue_len)

if queued < 100, do: raise("expected the mailbox to accumulate work")

IO.puts("slow actor accumulated #{queued} mailbox messages")
