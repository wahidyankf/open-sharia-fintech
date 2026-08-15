# Example 51 is Windows PowerShell only.
# => Built-in cmdlets inspect Windows state without a third-party module.
Get-Service | Where-Object Status -eq Running | Select-Object -First 5 Status, Name
# => The displayed values are observations; inspect errors before drawing conclusions.

