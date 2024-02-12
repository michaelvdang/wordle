cat $ENV_FILE_PATH > .env
cat $ENV_FILE_PATH > app/services/Stats/.env
cat $ENV_FILE_PATH > app/services/Play/.env
cat $REDIS_CONF_FILE_PATH > app/services/Redis/redis.conf