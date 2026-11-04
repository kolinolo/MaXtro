#!/bin/bash
clear


source /opt/MaXtro/scripts/.env


echo "Inicializando prune local"
restic forget --keep-within 14d --keep-daily 90 --keep-monthly 9999 --prune



