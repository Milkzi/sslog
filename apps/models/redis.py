import socket
import redis
from setting import REDIS_URI

pool = redis.ConnectionPool(host=REDIS_URI, port=6379, db=2, decode_responses=True)
r = redis.Redis(connection_pool=pool, encoding_errors='ignore',
                socket_timeout=3, socket_connect_timeout=2,
                health_check_interval=30, retry_on_timeout=True, socket_keepalive=True,
                #     socket_keepalive_options={            socket.TCP_KEEPIDLE:120,
                # socket.TCP_KEEPCNT:2,
                # socket.TCP_KEEPINTVL:30}
                )
