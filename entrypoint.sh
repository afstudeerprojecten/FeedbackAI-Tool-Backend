#!/bin/sh
python3 -m alembic upgrade head
python3 -m uvicorn app.main:app --host 0.0.0.0 --log-level INFO