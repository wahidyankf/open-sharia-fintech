pid=spawn(fn -> :ok end); ref=Process.monitor(pid); receive do {:DOWN,^ref,:process,^pid,_}->IO.puts("observed") end
