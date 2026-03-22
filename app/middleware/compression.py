"""GZip response compression."""

from starlette.middleware.gzip import GZipMiddleware

CompressionMiddleware = GZipMiddleware
