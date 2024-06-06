#!/bin/sh

set -e

. /venv/bin/activate
uvicorn main:app
exec "$@"