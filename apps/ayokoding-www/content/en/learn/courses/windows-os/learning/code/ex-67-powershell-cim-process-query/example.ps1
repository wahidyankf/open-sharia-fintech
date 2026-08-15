# Example 67 uses built-in Windows CIM data.
# => The current PowerShell process is a stable self-contained target.
Get-CimInstance Win32_Process -Filter "ProcessId = $PID" | Select-Object ProcessId, ParentProcessId, Name, CommandLine
# => CIM supplies parent and command-line observations alongside the native Win32 examples.
