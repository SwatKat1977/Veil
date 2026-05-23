export PYTHONPATH=.
export QUART_APP=veil/identity_service
#set SVC_CONFIG_FILE_REQUIRED=1
#set SVC_CONFIG_FILE=configs/svc.cfg
export BACKEND_DB_FILENAME=databases/identity_LATEST.db
export LOGGING_LOG_LEVEL=DEBUG

python -m veil.identity_service.run
