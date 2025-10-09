# ==========================================
# PubMed Knowledge Graph - Full Pipeline
# Runs Layers 1 → 3 automatically
# ==========================================

Write-Host '--------------------------------------'
Write-Host '🚀 Starting PubMed KG Pipeline...' -ForegroundColor Cyan
Write-Host '--------------------------------------'
Write-Host ''

# Layer 1: Ingestion
python ingestion/pubmed_fetch.py
if (-not $?) {
    Write-Host '❌ Layer 1 failed. Exiting.' -ForegroundColor Red
    exit
}

# Layer 2: NLP Extraction
python nlp_extraction/nlp_extractor.py
if (-not $?) {
    Write-Host '❌ Layer 2 failed. Exiting.' -ForegroundColor Red
    exit
}

# Layer 3: ETL + Storage
python etl/etl_transform.py --input data/extracted/nlp_extracted_*.json
if (-not $?) {
    Write-Host '❌ Layer 3 failed. Exiting.' -ForegroundColor Red
    exit
}

# Layer 3b: Verification
python etl/verify_etl.py
if (-not $?) {
    Write-Host '❌ Verification failed.' -ForegroundColor Red
    exit
}

Write-Host ''
Write-Host '✅ All layers completed successfully!' -ForegroundColor Green
Write-Host '--------------------------------------'
Write-Host '📊 Check your results in: data/storage/pubmed_etl.db'
Write-Host '--------------------------------------'
