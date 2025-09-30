# Ścieżka do katalogu bazowego
$basePath = "C:/Users/engli/fiszki/fiszki/zadanie rekrutacyjne/app"

# Ścieżka do pliku wynikowego (musi być plik, nie katalog)
$outputFile = "C:/Users/engli/fiszki/fiszki/zadanie rekrutacyjne/scripts/export.txt"

# Rozszerzenia plików, które chcemy przeszukać
$extensions = @("*.py", "*.json")

# Wyczyść plik wyjściowy jeśli istnieje
if (Test-Path $outputFile) {
    Clear-Content $outputFile
} else {
    New-Item -ItemType File -Path $outputFile -Force | Out-Null
}

foreach ($ext in $extensions) {
    Get-ChildItem -Path $basePath -Recurse -Include $ext -File | ForEach-Object {
        Add-Content -Path $outputFile -Value "`n##########################################"
        Add-Content -Path $outputFile -Value "# FILE: $($_.FullName)"
        Add-Content -Path $outputFile -Value "##########################################`n"
        Get-Content $_.FullName | Add-Content -Path $outputFile
    }
}

Write-Host "Eksport zakonczony. Plik wynikowy: $outputFile"
