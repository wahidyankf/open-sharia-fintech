# ex 33 handle call backpressure: explicit GenServer lifecycle behavior.
# backpressure: this line participates in queued synchronous work.
defmodule Queue do
# ex 33 handle call backpressure: explicit GenServer lifecycle behavior.
# backpressure: this line participates in queued synchronous work.
  use GenServer
# ex 33 handle call backpressure: explicit GenServer lifecycle behavior.
# backpressure: this line participates in queued synchronous work.
  def init(_), do: {:ok,0}
# ex 33 handle call backpressure: explicit GenServer lifecycle behavior.
# backpressure: this line participates in queued synchronous work.
  def handle_call(:work,_from,state) do
# backpressure: this line participates in queued synchronous work.
    Process.sleep(5)
# backpressure: this line participates in queued synchronous work.
    {:reply,state,state+1}
# backpressure: this line participates in queued synchronous work.
  end
# ex 33 handle call backpressure: explicit GenServer lifecycle behavior.
# backpressure: this line participates in queued synchronous work.
end
# ex 33 handle call backpressure: explicit GenServer lifecycle behavior.
# backpressure: this line participates in queued synchronous work.
{:ok,pid}=GenServer.start_link(Queue,nil)
# ex 33 handle call backpressure: explicit GenServer lifecycle behavior.
# backpressure: this line participates in queued synchronous work.
results=for _<-1..2, do: Task.async(fn->GenServer.call(pid,:work) end)
# ex 33 handle call backpressure: explicit GenServer lifecycle behavior.
# backpressure: this line participates in queued synchronous work.
IO.inspect(Enum.map(results,&Task.await/1))
