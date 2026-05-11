@echo off
echo Starting Veil - Identity Service
set PYTHONPATH=.
set QUART_APP=veil/identity_service
rem set SVC_CONFIG_FILE_REQUIRED=1
rem set SVC_CONFIG_FILE=configs/svc.cfg
rem set BACKEND_DB_FILENAME=databases/svc.LATEST.db
set LOGGING_LOG_LEVEL=DEBUG

python -m veil.identity_service.run
