# Windows version of the third CG Ember safety check (hooks/hooks.json, third PreToolUse entry).
# Reads the tool call from standard input and exits 0 only when tool_input.info is a JSON object,
# or a string holding one, whose "draft" field is exactly true, the same test as the Mac and Linux
# command. Field names are matched case-sensitively, as Python's json does. It prints nothing: the
# command in hooks.json prints the reason for any exit other than 0, so a script that cannot run
# at all also refuses, with the same reason.
# Each piece of JSON is checked to be an object before it is parsed. PowerShell 7 unrolls a
# top-level array when parsing, so '[{"draft":true}]' would otherwise reach the test as an object.
function Read-Object($text) {
    if ($text -isnot [string] -or -not $text.TrimStart().StartsWith('{')) { throw "not an object" }
    $parsed = ConvertFrom-Json -InputObject $text
    if ($parsed -isnot [System.Management.Automation.PSCustomObject]) { throw "not an object" }
    return $parsed
}
function Get-Field($obj, $name) {
    if ($obj -isnot [System.Management.Automation.PSCustomObject]) { throw "not an object" }
    $found = @($obj.PSObject.Properties | Where-Object { $_.Name -ceq $name })
    if ($found.Count -ne 1) { throw "no field $name" }
    # The comma keeps a one-item array an array; a plain return would unroll it into its item.
    return ,($found[0].Value)
}
try {
    $call = Read-Object ([Console]::In.ReadToEnd())
    $info = Get-Field (Get-Field $call 'tool_input') 'info'
    if ($info -is [string]) { $info = Read-Object $info }
    $draft = Get-Field $info 'draft'
    if ($draft -is [bool] -and $draft -eq $true) { exit 0 }
} catch {
}
exit 2
