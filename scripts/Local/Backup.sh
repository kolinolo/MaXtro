
restic -r $env:B2_RESTIC_REPOSITORY backup "$raiz" --dry-run
exit $LASTEXITCODE

