import redis.asyncio as aioredis

async def get_redis_client():
    redis_client = aioredis.Redis(
        host="redis.foodteacher.xyz",
        port=31436,
        decode_responses=True,
        retry_on_timeout=True,
        health_check_interval=30
    )
    try:
        yield redis_client
    finally:
        await redis_client.close()
