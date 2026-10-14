#!/bin/bash
clear


source /opt/MaXtro/scripts/.env

echo "Iniciando backup em: $RESTIC_REPOSITORY"


restic backup /export/Ethos/ --tag "pastas Ethos local"
echo ""
echo "Iniciando backup cloud"

restic -r $B2_RESTIC_REPOSITORY backup /export/Ethos/ --tag "pastas Ethos b2"

echo ""
echo "Inicializando prune local"

restic forget --keep-within 14d --keep-daily 90 --keep-monthly 9999 --prune