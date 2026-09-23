param(
  [Parameter(Mandatory = $true)]
  [ValidateSet("validate", "install")]
  [string]$Command,

  [string]$State,
  [string]$Candidate,
  [string]$Target = ".friday/state.json",
  [string]$Repo = "."
)

$ErrorActionPreference = "Stop"

function Get-Sha256([string]$Path) {
  return "sha256:" + (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Read-State([string]$Path) {
  if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
    throw "state file not found: $Path"
  }

  $raw = Get-Content -Raw -Encoding UTF8 -LiteralPath $Path
  $trimmed = $raw.TrimStart()

  if (-not $trimmed.StartsWith("{")) {
    throw "state root must be a JSON object"
  }

  return $raw | ConvertFrom-Json
}

function Resolve-RepoPath([string]$RepoRoot, [string]$Path) {
    if ([System.IO.Path]::IsPathRooted($Path)) {
        return [System.IO.Path]::GetFullPath($Path)
    }

    return [System.IO.Path]::GetFullPath((Join-Path $RepoRoot $Path))
}

function Resolve-DocumentPath([string]$RepoRoot, [string]$RelativePath) {
    if ([System.IO.Path]::IsPathRooted($RelativePath)) {
        throw "document path must be repository-relative: $RelativePath"
    }

    $trimChars = [char[]]@(
        [System.IO.Path]::DirectorySeparatorChar,
        [System.IO.Path]::AltDirectorySeparatorChar
    )
    $repoFull = [System.IO.Path]::GetFullPath($RepoRoot).TrimEnd($trimChars)
    $fullPath = [System.IO.Path]::GetFullPath((Join-Path $repoFull $RelativePath))
    $repoPrefix = $repoFull + [System.IO.Path]::DirectorySeparatorChar
    $comparison = if ([System.Environment]::OSVersion.Platform -eq [System.PlatformID]::Win32NT) {
        [System.StringComparison]::OrdinalIgnoreCase
    }
    else {
        [System.StringComparison]::Ordinal
    }

    if (
        $fullPath -ne $repoFull -and
        -not $fullPath.StartsWith($repoPrefix, $comparison)
    ) {
        throw "document path escapes repository: $RelativePath"
    }

    return $fullPath
}

function Validate-State($StateObject, [string]$RepoRoot) {
    $required = @(
        "version",
        "generated_by",
        "baseline",
        "project",
        "canonical_sources",
        "documents",
        "claims",
        "change_rules",
        "documentation_decisions",
        "unknowns"
    )

    if ($null -eq $StateObject -or $StateObject -isnot [PSCustomObject]) {
        throw "state root must be a JSON object"
    }

    $names = @($StateObject.PSObject.Properties.Name)
    foreach ($key in $required) {
        if ($names -notcontains $key) {
            throw "missing top-level key: $key"
        }
    }

    if ($StateObject.version -ne 1) {
        throw "unsupported state version"
    }

    if ($null -eq $StateObject.project -or $StateObject.project -isnot [PSCustomObject]) {
        throw "project must be an object"
    }

    $scopes = $StateObject.project.scopes
    if ($null -eq $scopes) {
        $scopes = @()
    }
    elseif ($scopes -isnot [System.Array]) {
        throw "project.scopes must be an array"
    }

    $scopeIds = @()

    foreach ($scope in $scopes) {
        if ($null -eq $scope -or $scope -isnot [PSCustomObject]) {
            throw "every scope must be an object with id"
        }

        if (-not $scope.id) {
            throw "every scope must be an object with id"
        }

        $scopeIds += $scope.id
    }

    if (@($scopeIds | Group-Object | Where-Object Count -gt 1).Count -gt 0) {
        throw "duplicate scope ids"
    }

    $scopeGroups = @(
        @{
            Label = "critical mechanism"
            Value = $StateObject.project.critical_mechanisms
            Optional = $true
        },
        @{
            Label = "canonical source"
            Value = $StateObject.canonical_sources
            Optional = $false
        },
        @{
            Label = "document"
            Value = $StateObject.documents
            Optional = $false
        },
        @{
            Label = "unknown"
            Value = $StateObject.unknowns
            Optional = $false
        }
    )

    foreach ($entry in $scopeGroups) {
        $group = $entry.Value

        if ($null -eq $group -and $entry.Optional) {
            $group = @()
        }
        elseif ($group -isnot [System.Array]) {
            throw "$($entry.Label) collection must be an array"
        }

        foreach ($item in $group) {
            if ($null -eq $item -or $item -isnot [PSCustomObject]) {
                throw "$($entry.Label) item must be an object"
            }

            if ($null -ne $item.scope -and $scopeIds -notcontains $item.scope) {
                throw "$($entry.Label) references unknown scope: $($item.scope)"
            }
        }
    }

    $claims = $StateObject.claims

    if ($claims -isnot [System.Array]) {
        throw "claims must be an array"
    }

    $claimIds = @()

    foreach ($claim in $claims) {
        if ($null -eq $claim -or $claim -isnot [PSCustomObject]) {
            throw "every claim must be an object with id"
        }

        if (-not $claim.id) {
            throw "every claim must be an object with id"
        }

        $claimIds += $claim.id
    }

    if (@($claimIds | Group-Object | Where-Object Count -gt 1).Count -gt 0) {
        throw "duplicate claim ids"
    }

    $docPaths = @()

    foreach ($doc in $StateObject.documents) {
        if (-not $doc.path) {
            throw "document missing path"
        }

        $docPaths += $doc.path
        $fullPath = Resolve-DocumentPath $RepoRoot $doc.path

        foreach ($claimId in @($doc.related_claims)) {
            if ($claimIds -notcontains $claimId) {
                throw "$($doc.path) references unknown claim: $claimId"
            }
        }

        if ($doc.ownership -eq "managed") {
            if (-not (Test-Path -LiteralPath $fullPath -PathType Leaf)) {
                throw "managed document missing: $($doc.path)"
            }

            if ($doc.content_hash) {
                $actual = Get-Sha256 $fullPath

                if ($doc.content_hash.ToLowerInvariant() -ne $actual) {
                    throw "managed document hash mismatch for $($doc.path)"
                }
            }
        }
    }

    foreach ($claim in $claims) {
        foreach ($docPath in @($claim.documents)) {
            if ($docPaths -notcontains $docPath) {
                throw "claim $($claim.id) references unknown document: $docPath"
            }
        }
    }
}

function Write-CanonicalJson($Object, [string]$Path) {
  $json = $Object | ConvertTo-Json -Depth 100
  [System.IO.File]::WriteAllText(
    $Path,
    $json + [Environment]::NewLine,
    [System.Text.UTF8Encoding]::new($false)
  )
}

$repoRoot = (Resolve-Path -LiteralPath $Repo).Path

if ($Command -eq "validate") {
  if (-not $State) {
    throw "-State is required for validate"
  }

  $stateObject = Read-State $State
  Validate-State $stateObject $repoRoot
  Write-Output "state valid"
  exit 0
}

if (-not $Candidate) {
  throw "-Candidate is required for install"
}

$candidatePath = Resolve-RepoPath $repoRoot $Candidate
$candidateObject = Read-State $candidatePath
Validate-State $candidateObject $repoRoot

$targetPath = Resolve-RepoPath $repoRoot $Target
$targetDir = Split-Path -Parent $targetPath
if (-not $targetDir) {
  $targetDir = "."
}
New-Item -ItemType Directory -Force -Path $targetDir | Out-Null

$temp = Join-Path $targetDir ((Split-Path -Leaf $targetPath) + "." + [guid]::NewGuid().ToString("N") + ".tmp")
try {
  Copy-Item -LiteralPath $candidatePath -Destination $temp -Force

  $roundTrip = Read-State $temp
  Validate-State $roundTrip $repoRoot

  Move-Item -LiteralPath $temp -Destination $targetPath -Force
}
finally {
  if (Test-Path -LiteralPath $temp -PathType Leaf) {
    Remove-Item -LiteralPath $temp -Force
  }
}
Write-Output "state installed: $Target"
