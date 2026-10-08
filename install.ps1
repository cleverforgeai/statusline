# Made by CleverForge (github.com/CleverForgeAI). Private repository.
# Installer for Windows PowerShell.
# Private repo, recommended: clone it, then install from the local folder.
#   gh repo clone cleverforgeai/statusline; cd statusline; $env:STATUSLINE_LOCAL=$PWD; .\install.ps1
# Env: STATUSLINE_REPO, STATUSLINE_BASE, STATUSLINE_TOKEN (GitHub token), STATUSLINE_LOCAL, STATUSLINE_REFRESH.
# Requires Python 3 and Git on PATH. Git Bash is used to run the wrapper.
$ErrorActionPreference = 'Stop'
$Repo = if ($env:STATUSLINE_REPO) { $env:STATUSLINE_REPO } else { 'cleverforgeai/statusline' }
$Base = if ($env:STATUSLINE_BASE) { $env:STATUSLINE_BASE } else { "https://raw.githubusercontent.com/$Repo/main" }
$Dest = Join-Path $env:USERPROFILE '.claude'
$Settings = Join-Path $Dest 'settings.json'

if (-not (Get-Command python -ErrorAction SilentlyContinue)) { throw 'Python 3 is required (command: python).' }
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { Write-Warning 'git not found. Git and GitHub segments will be empty.' }
$bash = Get-Command bash -ErrorAction SilentlyContinue
if (-not $bash) { Write-Warning 'bash not found. Install Git for Windows so the wrapper can run.' }

New-Item -ItemType Directory -Force -Path (Join-Path $Dest 'skills\statusline') | Out-Null

function Get-Remote($rel, $out) {
  if ($env:STATUSLINE_LOCAL) { Copy-Item (Join-Path $env:STATUSLINE_LOCAL $rel) $out -Force }
  elseif ($env:STATUSLINE_TOKEN) { Invoke-WebRequest "$Base/$rel" -OutFile $out -UseBasicParsing -Headers @{ Authorization = "token $($env:STATUSLINE_TOKEN)" } }
  else { Invoke-WebRequest "$Base/$rel" -OutFile $out -UseBasicParsing }
}

foreach ($f in 'statusline.py','statusline-command.sh') {
  $p = Join-Path $Dest $f
  if (Test-Path $p) { Copy-Item $p "$p.bak" -Force }
  Get-Remote $f $p
}
Get-Remote 'skill/SKILL.md' (Join-Path $Dest 'skills\statusline\SKILL.md')

$cfg = Join-Path $Dest 'statusline.config.json'
if (-not (Test-Path $cfg)) {
  [System.IO.File]::WriteAllText($cfg, '{ "apps": {}, "show_github": true, "show_tasks": true, "show_memory": false, "two_lines": true, "fun_line": true, "animate": true, "sprite": "car", "sprite_chosen": false, "setup_done": false, "flags": [], "compact_alert": true, "fav_reminder": true, "org": "", "life_source": "context" }', (New-Object System.Text.UTF8Encoding($false)))
}

$cmd = 'bash ' + ($Dest -replace '\\','/') + '/statusline-command.sh'
if (Test-Path $Settings) { Copy-Item $Settings "$Settings.bak" -Force; $json = Get-Content $Settings -Raw | ConvertFrom-Json } else { $json = [pscustomobject]@{} }
$refresh = if ($env:STATUSLINE_REFRESH) { [int]$env:STATUSLINE_REFRESH } else { 1 }   # seconds; 0 turns the timer off
$sl = [pscustomobject]@{ type = 'command'; command = $cmd }
if ($refresh -gt 0) { $sl | Add-Member -NotePropertyName refreshInterval -NotePropertyValue $refresh }
if ($json.PSObject.Properties.Name -contains 'statusLine') { $json.statusLine = $sl } else { $json | Add-Member -NotePropertyName statusLine -NotePropertyValue $sl }
[System.IO.File]::WriteAllText($Settings, ($json | ConvertTo-Json -Depth 20), (New-Object System.Text.UTF8Encoding($false)))   # no BOM

Write-Host 'Statusline Kit installed. Made by CleverForge.'
Write-Host 'Restart Claude Code (or open a new session) to see the status line.'
Write-Host 'Last step: open Claude Code and type /statusline. Claude asks a few quick questions and sets it all up.'
Write-Host "Edit $cfg to name your apps. Run /statusline in Claude Code to adjust."
