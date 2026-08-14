import asyncio
import random
import statistics
import time
from collections import Counter

import httpx

URL = "http://localhost:8000/chat"

QUESTIONS = [
    "What is artificial intelligence?",
    "Explain FastAPI.",
    "What is Docker?",
    "How does RAG work?",
    "What is observability?",
    "Explain Prometheus metrics.",
    "What is Grafana?",
    "How does vector search work?",
    "Difference between REST and GraphQL?",
    "What is PostgreSQL?"
]

# -----------------------
# Configuration
# -----------------------

REQUESTS_PER_SECOND = 10
DURATION_SECONDS = 30
MAX_CONCURRENCY = 20

TOTAL_REQUESTS = REQUESTS_PER_SECOND * DURATION_SECONDS

timeout = httpx.Timeout(
    connect=10,
    read=120,
    write=30,
    pool=30,
)

limits = httpx.Limits(
    max_connections=100,
    max_keepalive_connections=50,
)

# -----------------------
# Statistics
# -----------------------

latencies = []
status_counter = Counter()
error_counter = Counter()

completed = 0
lock = asyncio.Lock()

semaphore = asyncio.Semaphore(MAX_CONCURRENCY)


async def send_request(client: httpx.AsyncClient, request_id: int):
    global completed

    async with semaphore:

        payload = {
            "question": random.choice(QUESTIONS)
        }

        start = time.perf_counter()

        try:
            response = await client.post(
                URL,
                json=payload,
            )

            duration = (time.perf_counter() - start) * 1000

            latencies.append(duration)
            status_counter[response.status_code] += 1

            print(
                f"[{request_id:03}] "
                f"{response.status_code} "
                f"{duration:.0f} ms"
            )

        except Exception as exc:
            error_counter[type(exc).__name__] += 1

            print(
                f"[{request_id:03}] "
                f"ERROR: {type(exc).__name__}"
            )

        finally:
            async with lock:
                completed += 1


async def main():

    print("=" * 60)
    print("AI Gateway Load Test")
    print("=" * 60)
    print(f"Target RPS       : {REQUESTS_PER_SECOND}")
    print(f"Duration         : {DURATION_SECONDS} sec")
    print(f"Concurrency      : {MAX_CONCURRENCY}")
    print(f"Total Requests   : {TOTAL_REQUESTS}")
    print("=" * 60)

    async with httpx.AsyncClient(
        timeout=timeout,
        limits=limits,
    ) as client:

        tasks = []

        interval = 1 / REQUESTS_PER_SECOND

        for request_id in range(TOTAL_REQUESTS):

            tasks.append(
                asyncio.create_task(
                    send_request(client, request_id)
                )
            )

            await asyncio.sleep(interval)

        await asyncio.gather(*tasks)

    print("\n")
    print("=" * 60)
    print("Summary")
    print("=" * 60)

    success = sum(status_counter.values())
    failed = sum(error_counter.values())

    print(f"Successful : {success}")
    print(f"Failed     : {failed}")

    print()

    for status, count in sorted(status_counter.items()):
        print(f"HTTP {status:<3} : {count}")

    print()

    for error, count in error_counter.items():
        print(f"{error:<15}: {count}")

    if latencies:
        print()
        print(f"Average Latency : {statistics.mean(latencies):.0f} ms")
        print(f"Minimum Latency : {min(latencies):.0f} ms")
        print(f"Maximum Latency : {max(latencies):.0f} ms")

        if len(latencies) >= 20:
            p95 = statistics.quantiles(latencies, n=100)[94]
            p99 = statistics.quantiles(latencies, n=100)[98]

            print(f"P95 Latency     : {p95:.0f} ms")
            print(f"P99 Latency     : {p99:.0f} ms")

    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())