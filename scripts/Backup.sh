#!/bin/bash
clear


source /opt/MaXtro/scripts/.env

echo "Iniciando backup em: $RESTIC_REPOSITORY"


restic backup /export/Ethos/ --tag "pastas Ethos local" --dry-run

