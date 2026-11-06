# syntax=docker/dockerfile:1

# Stage 1: Dependency builder
FROM python:3.13-slim@sha256:09a17cad02668ae61ece136b4fd36ac3849e14f670ebedb637ea3e15580525bc AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

COPY requirements.txt .

RUN python -m pip install \
    --no-cache-dir \
    --prefix=/install \
    -r requirements.txt


# Stage 2: Production runtime
FROM python:3.13-slim@sha256:09a17cad02668ae61ece136b4fd36ac3849e14f670ebedb637ea3e15580525bc AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /opt/app

# Apply the verified Debian APT security fix.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       apt=3.0.4 \
       libapt-pkg7.0=3.0.4 \
    && rm -rf /var/lib/apt/lists/*

# Copy only installed application dependencies.
COPY --from=builder /install/ /usr/local/

# Remove pip from the active runtime filesystem.
RUN python -m pip uninstall -y pip \
    && useradd \
       --uid 10001 \
       --create-home \
       --shell /usr/sbin/nologin \
       appuser

COPY --chown=10001:10001 service ./service

USER 10001:10001

EXPOSE 8080

CMD ["uvicorn", "service.main:app", "--host", "0.0.0.0", "--port", "8080"]
