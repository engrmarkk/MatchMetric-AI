#!/bin/bash

#uvicorn resumeai_proj.asgi:application --reload --lifespan off
gunicorn -w 4 -k uvicorn.workers.UvicornWorker resumeai_proj.asgi:application --timeout 120
