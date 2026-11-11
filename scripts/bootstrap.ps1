[CmdletBinding()]
param(
    [string]$CodexHome,
    [switch]$SkipCore
)

$ErrorActionPreference = 'Stop'
$RepoRoot = Split-Path $PSScriptRoot -Parent

if (-not $CodexHome) {
    $CodexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
}

$SkillsRoot = Join-Path $CodexHome 'skills'
New-Item -ItemType Directory -Path $SkillsRoot -Force | Out-Null

function Install-DirectorySafely {
    param(
        [Parameter(Mandatory)] [string]$Source,
        [Parameter(Mandatory)] [string]$Name
    )

    $Destination = Join-Path $SkillsRoot $Name
    if (Test-Path -LiteralPath $Destination) {
        Write-Output "SKIP $Name (destination already exists: $Destination)"
        return
    }

    if (-not (Test-Path -LiteralPath (Join-Path $Source 'SKILL.md'))) {
        throw "Refusing to install $Name because SKILL.md was not found in $Source"
    }

    Copy-Item -LiteralPath $Source -Destination $Destination -Recurse
    Write-Output "INSTALLED $Name -> $Destination"
}

$RouterSource = Join-Path $RepoRoot 'skills\starred-skill-router'
Install-DirectorySafely -Source $RouterSource -Name 'starred-skill-router'

if (-not $SkipCore) {
    $Manifest = Join-Path $RepoRoot 'config\core-skills.tsv'
    $Entries = Import-Csv -LiteralPath $Manifest -Delimiter "`t"

    foreach ($Entry in $Entries) {
        $Destination = Join-Path $SkillsRoot $Entry.name
        if (Test-Path -LiteralPath $Destination) {
            Write-Output "SKIP $($Entry.name) (destination already exists: $Destination)"
            continue
        }

        $TempBase = [System.IO.Path]::GetTempPath()
        $TempPath = Join-Path $TempBase ("codex-powerpack-" + [guid]::NewGuid().ToString('N'))
        New-Item -ItemType Directory -Path $TempPath | Out-Null

        try {
            $Archive = Join-Path $TempPath 'source.zip'
            $Extract = Join-Path $TempPath 'extract'
            $Url = "https://codeload.github.com/$($Entry.repo)/zip/$($Entry.commit)"
            Write-Output "DOWNLOAD $($Entry.name) from $($Entry.repo)@$($Entry.commit)"
            Invoke-WebRequest -Uri $Url -OutFile $Archive -UseBasicParsing
            Expand-Archive -LiteralPath $Archive -DestinationPath $Extract

            $ArchiveRoot = Get-ChildItem -LiteralPath $Extract -Directory | Select-Object -First 1
            if (-not $ArchiveRoot) {
                throw "The archive for $($Entry.name) did not contain a root directory."
            }

            $Source = if ($Entry.path -eq '.') {
                $ArchiveRoot.FullName
            } else {
                Join-Path $ArchiveRoot.FullName ($Entry.path -replace '/', '\')
            }

            Install-DirectorySafely -Source $Source -Name $Entry.name
        }
        finally {
            $ResolvedTempBase = [System.IO.Path]::GetFullPath($TempBase)
            $ResolvedTempPath = [System.IO.Path]::GetFullPath($TempPath)
            if ($ResolvedTempPath.StartsWith($ResolvedTempBase, [System.StringComparison]::OrdinalIgnoreCase) -and
                (Split-Path $ResolvedTempPath -Leaf).StartsWith('codex-powerpack-')) {
                Remove-Item -LiteralPath $ResolvedTempPath -Recurse -Force -ErrorAction SilentlyContinue
            }
        }
    }
}

Write-Output ''
Write-Output "Codex Powerpack is installed in $SkillsRoot"
Write-Output 'Open a new Codex chat before relying on newly installed skill discovery.'

