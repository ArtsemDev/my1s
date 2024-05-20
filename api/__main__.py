from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from api import v1

app = FastAPI()
app.include_router(router=v1.router, prefix="/api")
app.add_middleware(middleware_class=GZipMiddleware)
app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=("*", ),
    allow_methods=("*", ),
    allow_headers=("*", ),
)
app.add_middleware(
    middleware_class=ProxyHeadersMiddleware,
    trusted_hosts=("*", )
)


if __name__ == '__main__':
    from uvicorn import run
    run(app=app, host="0.0.0.0", port=80)
