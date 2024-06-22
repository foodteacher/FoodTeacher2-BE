import redis

pool = redis.ConnectionPool(
    host="redis.foodteacher.xyz",
    port=31436,
    decode_responses=True,
    retry_on_timeout=True,
    health_check_interval=30
)

r = redis.Redis(connection_pool=pool)