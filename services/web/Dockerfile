FROM python:3.10-alpine AS build


ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	PYTHONPATH=/src \
	POETRY_VERSION=1.1.11 \
	POETRY_VIRTUALENVS_CREATE=false \
	POETRY_NO_INTERACTION=1 \
	POETRY_CACHE_DIR='/var/cache/pypoetry' \
	POETRY_HOME='/opt/poetry' \
	PATH="$POETRY_HOME/bin:$PATH" \
	USER=appuser

WORKDIR ${PYTHONPATH}

COPY . ${PYTHONPATH}

# Install Sys dependencies
RUN apk add --no-cache postgresql-libs && \
	apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
	pip install poetry && \
	poetry install --only main && \
	apk --purge del .build-deps && \
	rm -rf $POETRY_CACHE_DIR

FROM build AS output

WORKDIR ${PYTHONPATH}

COPY --from=build /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=build /usr/local/bin /usr/local/bin
COPY --from=build ${PYTHONPATH} ${PYTHONPATH}


# Entrypoint to handle Database Connection & migrations
ENTRYPOINT [ "/src/entrypoint.sh" ]

# Run the app
CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--no-server-header"]