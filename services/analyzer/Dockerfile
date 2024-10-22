FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml ./
COPY solprobe_analyzer ./solprobe_analyzer
RUN pip install --no-cache-dir .
CMD ["python", "-m", "celery", "-A", "solprobe_analyzer.celery_app", "worker", "--loglevel=info"]
