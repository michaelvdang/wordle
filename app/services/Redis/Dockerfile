# only run in Jenkins testing
FROM redis:alpine
COPY ./redis.conf /usr/local/etc/redis/redis.conf
RUN rm -r logs
CMD [ "redis-server", "/usr/local/etc/redis/redis.conf" ]
