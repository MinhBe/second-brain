param([ValidateSet('DryRun','Apply','Rollback')][string]$Mode='DryRun', [string]$Manifest=(Join-Path $PSScriptRoot 'moves.json'))
$ErrorActionPreference='Stop'
$data=Get-Content -Raw -Encoding UTF8 -LiteralPath $Manifest | ConvertFrom-Json
$collectionRoot=[IO.Path]::GetFullPath($data.root).TrimEnd('\')
$rootPrefix=$collectionRoot+'\'
$operations=@($data.moves)
if($Mode -eq 'Rollback'){[array]::Reverse($operations)}
$checked=@()
foreach($operation in $operations){
    $sourceRelative=$operation.source
    $targetRelative=$operation.destination
    if($Mode -eq 'Rollback'){$sourceRelative=$operation.destination; $targetRelative=$operation.source}
    $source=[IO.Path]::GetFullPath((Join-Path $collectionRoot $sourceRelative))
    $target=[IO.Path]::GetFullPath((Join-Path $collectionRoot $targetRelative))
    if(!$source.StartsWith($rootPrefix,[StringComparison]::OrdinalIgnoreCase) -or !$target.StartsWith($rootPrefix,[StringComparison]::OrdinalIgnoreCase)){
        throw 'A move escapes the Collection root'
    }
    foreach($path in @($source,$target)){
        $ancestor=$path
        while($ancestor -ne $collectionRoot){
            if(Test-Path -LiteralPath $ancestor){
                $item=Get-Item -Force -LiteralPath $ancestor
                if($item.Attributes -band [IO.FileAttributes]::ReparsePoint){throw "Reparse point in move path: $ancestor"}
            }
            $ancestor=Split-Path -Parent $ancestor
            if(!$ancestor){throw 'Invalid ancestor'}
        }
    }
    $sourceExists=Test-Path -LiteralPath $source
    $targetExists=Test-Path -LiteralPath $target
    if($sourceExists -and $targetExists){throw "Destination conflict: $target"}
    if(!$sourceExists -and !$targetExists){throw "Missing source and target: $source"}
    $checked+=@{source=$source; target=$target; completed=(!$sourceExists -and $targetExists)}
}
foreach($move in $checked){
    if($move.completed){Write-Output "Already moved: $($move.target)"; continue}
    if($Mode -eq 'DryRun'){Write-Output "$($move.source) -> $($move.target)"; continue}
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $move.target) | Out-Null
    Move-Item -LiteralPath $move.source -Destination $move.target
    $entry=@{time=(Get-Date -Format o);mode=$Mode;source=$move.source;target=$move.target}|ConvertTo-Json -Compress
    Add-Content -LiteralPath (Join-Path (Split-Path -Parent $Manifest) 'moves.executed.jsonl') -Value $entry -Encoding UTF8
    Write-Output "Moved: $($move.target)"
}
