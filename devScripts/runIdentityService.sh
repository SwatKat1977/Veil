export PYTHONPATH=.
export QUART_APP=veil/identity_service
#set SVC_CONFIG_FILE_REQUIRED=1
#set SVC_CONFIG_FILE=configs/svc.cfg
#set BACKEND_DB_FILENAME=databases/svc.LATEST.db
export LOGGING_LOG_LEVEL=DEBUG

quart run -p 5050 --reload
