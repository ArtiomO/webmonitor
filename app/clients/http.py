from dataclasses import dataclass

import aiohttp


@dataclass
class Trace:
    latency: int = None


class HttpClientConnectionError(Exception):
    pass


def request_tracer(results_collector: Trace):
    """Request tracing function."""

    async def on_request_start(session, context, params):
        context.on_request_start = session.loop.time()

    async def on_request_end(session, context, params):
        total = session.loop.time() - context.on_request_start
        results_collector.latency = int(round(total * 1000, 2))

    trace_config = aiohttp.TraceConfig()

    trace_config.on_request_start.append(on_request_start)
    trace_config.on_request_end.append(on_request_end)

    return trace_config


class HttpClient:
    """Http client with exception handling."""

    async def request(self, url: str, method: str) -> (int, dict):
        trace = Trace()
        try:
            async with aiohttp.ClientSession(
                trace_configs=[request_tracer(trace)]
            ) as session:
                async with session.request(method=method, url=url) as resp:
                    resp_body = await resp.text()
                    return resp.status, resp_body, trace.latency
        except aiohttp.ClientConnectionError:
            raise HttpClientConnectionError


http_client = HttpClient()
