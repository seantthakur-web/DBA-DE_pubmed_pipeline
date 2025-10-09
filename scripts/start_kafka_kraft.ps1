<#
    start_kafka_kraft.ps1
    ---------------------
    Runs a full Kafka (KRaft mode) startup on Windows:
        • Checks Kafka path
        • Initializes metadata (once)
        • Starts the broker (no ZooKeeper)
        • Creates topic "pubmed_raw"
        • Lists topics for verification
#>

# ---------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------
$KAFKA_HOME = "C:\kafka"
$CONFIG_FILE = "$KAFKA_HOME\config\kraft\server.properties"
$LOG_DIR = "$KAFKA_HOME\logs"
$TOPIC_NAME = "pubmed_raw"
$BROKER = "localhost:9092"

# ---------------------------------------------------------------
# 1️⃣  Validate Kafka folder
# ---------------------------------------------------------------
if (!(Test-Path $KAFKA_HOME)) {
    Write-Host "❌ Kafka not found at $KAFKA_HOME. Please adjust the path." -ForegroundColor Red
    exit
}

# ---------------------------------------------------------------
# 2️⃣  Initialize metadata (only first time)
# ---------------------------------------------------------------
$metaDir = "$KAFKA_HOME\kraft-combined-logs"
if (!(Test-Path $metaDir)) {
    Write-Host "🧩 Initializing Kafka metadata directory (first time only)..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Force -Path $metaDir | Out-Null
    Push-Location $KAFKA_HOME
    $guid = [guid]::NewGuid().ToString()
    & .\bin\windows\kafka-storage.bat format -t $guid -c $CONFIG_FILE
    Pop-Location
} else {
    Write-Host "✅ Metadata already initialized."
}

# ---------------------------------------------------------------
# 3️⃣  Start Kafka Broker (KRaft)
# ---------------------------------------------------------------
Write-Host "`n🚀 Starting Kafka in KRaft mode..." -ForegroundColor Green

if (!(Test-Path $LOG_DIR)) { New-Item -ItemType Directory -Path $LOG_DIR | Out-Null }

# Direct call avoids "input line too long"
$KafkaStart = Join-Path $KAFKA_HOME "bin\windows\kafka-server-start.bat"

$StartInfo = New-Object System.Diagnostics.ProcessStartInfo
$StartInfo.FileName = $KafkaStart
$StartInfo.Arguments = "`"$CONFIG_FILE`""
$StartInfo.WorkingDirectory = $KAFKA_HOME
$StartInfo.RedirectStandardOutput = $true
$StartInfo.RedirectStandardError  = $true
$StartInfo.UseShellExecute = $false
$StartInfo.CreateNoWindow = $true
$process = [System.Diagnostics.Process]::Start($StartInfo)

Write-Host "Kafka process ID: $($process.Id)"
Start-Sleep -Seconds 10

# ---------------------------------------------------------------
# 4️⃣  Create topic if it doesn’t exist
# ---------------------------------------------------------------
Write-Host "`n📦 Checking/creating topic '$TOPIC_NAME'..."
Push-Location $KAFKA_HOME
try {
    & .\bin\windows\kafka-topics.bat --create --topic $TOPIC_NAME --bootstrap-server $BROKER `
        --partitions 1 --replication-factor 1 2>$null
    Write-Host "✅ Topic '$TOPIC_NAME' created or already exists."
} catch {
    Write-Host "⚠️  Error creating topic: $_"
}
Pop-Location

# ---------------------------------------------------------------
# 5️⃣  List topics for verification
# ---------------------------------------------------------------
Write-Host "`n📋 Verifying topic list..."
Push-Location $KAFKA_HOME
& .\bin\windows\kafka-topics.bat --list --bootstrap-server $BROKER
Pop-Location

Write-Host "`n🎉 Kafka KRaft setup complete and ready for use!" -ForegroundColor Cyan
