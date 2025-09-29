# Dockerfile — Flask + Gunicorn
FROM python:3.12-slim

# 1) SO deps essenciais
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates build-essential \
  && rm -rf /var/lib/apt/lists/*

# 2) Usuário não-root
RUN groupadd -r appuser && useradd -r -g appuser appuser

# 3) Diretório de trabalho e envs base
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PORT=5000 \
    APP_MODULE="src.main:app" \
    GUNICORN_CMD_ARGS="--workers=${GUNICORN_WORKERS:-2} --threads=4 --timeout=120 --keep-alive=2 --max-requests=1000 --max-requests-jitter=100"

# 4) Dependências Python
COPY requirements.txt /app/requirements.txt
# Garanta que requirements.txt contém: Flask, Flask-Cors, Flask-SQLAlchemy, SQLAlchemy, gunicorn, psycopg2-binary
RUN pip install --no-cache-dir -r /app/requirements.txt

# 5) Código da aplicação
# Se TODO seu código está em src/, mantenha esta linha:
COPY src/ /app/src/
# Se houver outros diretórios/arquivos fora de src/ que a app usa, troque por:
# COPY . .

# 6) Permissões
RUN chown -R appuser:appuser /app
USER appuser

# 7) Healthcheck
# Opção A: manter se você tiver rota /api/health
# HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=5 \
#   CMD curl -fsS "http://127.0.0.1:${PORT:-5000}/api/health" || exit 1

# Opção B: checar a home (se serve index)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=5 \
  CMD curl -fsS "http://127.0.0.1:${PORT:-5000}/" || exit 1

# 8) Porta e comando de inicialização
EXPOSE 5000
CMD ["bash", "-lc", "gunicorn ${APP_MODULE:-src.main:app} --bind 0.0.0.0:${PORT:-5000} ${GUNICORN_CMD_ARGS}"]