#!/bin/bash

#gunicorn -w 4 -k uvicorn.workers.UvicornWorker resumeai_proj.asgi:application --timeout 120
uvicorn resumeai_proj.asgi:application --reload --port 8001