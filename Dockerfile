# Receta de la imagen del Dashboard de Works.
# Solo entra lo necesario para correr: app/, web/ y pyproject.toml (ver .dockerignore).
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=America/Mexico_City \
    WORKS_DB=/datos/works.db

WORKDIR /srv/works

# Dependencias de producción, leídas de pyproject.toml para no duplicarlas.
COPY pyproject.toml .
RUN python -c "import tomllib; print('\n'.join(tomllib.load(open('pyproject.toml', 'rb'))['project']['dependencies']))" > /tmp/requisitos.txt \
    && pip install --no-cache-dir -r /tmp/requisitos.txt tzdata \
    && rm /tmp/requisitos.txt

COPY app ./app
COPY web ./web

# Usuario sin privilegios; /datos guarda la base y la configuración de cuentas.
RUN useradd --create-home --uid 1000 works \
    && mkdir -p /datos \
    && chown works:works /datos
USER works

EXPOSE 8000

# Aplica las migraciones pendientes (no borra datos) y arranca el servicio.
CMD ["sh", "-c", "python -m app.db.migrar && exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --proxy-headers --forwarded-allow-ips='*'"]
