# Example 26 is Windows PowerShell only.
# => Built-in cmdlets inspect Windows state without a third-party module.
Get-ItemProperty -Path HKCU:\Environment | Select-Object -First 1
# => The displayed values are observations; inspect errors before drawing conclusions.

