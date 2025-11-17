$ErrorActionPreference = 'Stop'
Set-Location "C:\Users\rushi\Downloads\demo-2"

$domain = "https://html.awaikenthemes.com/primecare/demo-2"
$htmlFiles = Get-ChildItem -File -Recurse -Include *.html

# Ensure local asset folders
New-Item -ItemType Directory -Force -Path ".\images" | Out-Null
New-Item -ItemType Directory -Force -Path ".\js" | Out-Null
New-Item -ItemType Directory -Force -Path ".\css" | Out-Null

# Collect remote asset URLs
$imagesRegex = "https://html\.awaikenthemes\.com/primecare/demo-2/images/[^\"' >)]+"
$jsRegex     = "https://html\.awaikenthemes\.com/primecare/demo-2/js/[^\"' >)]+"
$cssRegex    = "https://html\.awaikenthemes\.com/primecare/demo-2/css/[^\"' >)]+"

$imgUrls = $htmlFiles | Select-String -Pattern $imagesRegex -AllMatches | ForEach-Object { $_.Matches } | ForEach-Object { $_.Value } | Sort-Object -Unique
$jsUrls  = $htmlFiles | Select-String -Pattern $jsRegex     -AllMatches | ForEach-Object { $_.Matches } | ForEach-Object { $_.Value } | Sort-Object -Unique
$cssUrls = $htmlFiles | Select-String -Pattern $cssRegex    -AllMatches | ForEach-Object { $_.Matches } | ForEach-Object { $_.Value } | Sort-Object -Unique

# Download assets locally
foreach ($url in $imgUrls) {
  $dest = Join-Path ".\images" (Split-Path $url -Leaf)
  if (-not (Test-Path $dest)) {
    try { Invoke-WebRequest -Uri $url -OutFile $dest -UseBasicParsing -TimeoutSec 60 }
    catch { Write-Warning "Failed image: $url" }
  }
}
foreach ($url in $jsUrls) {
  $dest = Join-Path ".\js" (Split-Path $url -Leaf)
  if (-not (Test-Path $dest)) {
    try { Invoke-WebRequest -Uri $url -OutFile $dest -UseBasicParsing -TimeoutSec 60 }
    catch { Write-Warning "Failed js: $url" }
  }
}
foreach ($url in $cssUrls) {
  $dest = Join-Path ".\css" (Split-Path $url -Leaf)
  if (-not (Test-Path $dest)) {
    try { Invoke-WebRequest -Uri $url -OutFile $dest -UseBasicParsing -TimeoutSec 60 }
    catch { Write-Warning "Failed css: $url" }
  }
}

# Rewrite references in HTML files to local assets and local pages
foreach ($f in $htmlFiles) {
  $c = Get-Content $f.FullName -Raw
  $c = $c -replace [Regex]::Escape($domain + "/images/"), "images/"
  $c = $c -replace [Regex]::Escape($domain + "/js/"), "js/"
  $c = $c -replace [Regex]::Escape($domain + "/css/"), "css/"
  $c = $c -replace [Regex]::Escape($domain + "/"), ""
  Set-Content $f.FullName $c -Encoding UTF8
}