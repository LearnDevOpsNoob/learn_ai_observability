from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

from time import perf_counter
from src.config.metrics import (
    HTTP_REQUEST_DURATION,
    HTTP_REQUESTS_IN_PROGRESS,
    HTTP_REQUESTS_TOTAL
)

class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        HTTP_REQUESTS_IN_PROGRESS.inc()

        start_time = perf_counter()

        response = None

        try:
            response = await call_next(request)
            return response
        finally:
            duration = perf_counter() - start_time

            HTTP_REQUESTS_IN_PROGRESS.dec()

            route = request.scope.get("route")

            endpoint = (route.path) if route is not None else request.url.path 

            method = request.method
            status = (
                str(response.status_code) if response else "500"
            )

            HTTP_REQUESTS_TOTAL.labels(
                method=method,
                endpoint=endpoint,
                status=status
            ).inc()

            HTTP_REQUEST_DURATION.labels(
                method=method,
                endpoint=endpoint
            ).observe(duration)






        return await super().dispatch(request, call_next)


