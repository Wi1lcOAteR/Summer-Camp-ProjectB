FROM --platform=linux/amd64 node:24.18.0-bookworm-slim@sha256:d45d78e7929b46875bbd4e29bea672d5bc48186c6c3588306521c815e78352d6 AS frontend-build
WORKDIR /src/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci --ignore-scripts --no-audit --no-fund
COPY frontend/ ./
RUN npm run build

FROM --platform=linux/amd64 python:3.14.6-slim-bookworm@sha256:f70215e5dbe2a47dee6d23f9c6d358bf3c148f59cce2fd165b61118e9d80f2bb AS python-deps
WORKDIR /opt/projectb
COPY packaging/oci/requirements.linux-demo.lock /tmp/requirements.linux-demo.lock
RUN python -m pip install --no-cache-dir --require-hashes --no-deps --only-binary=:all: --target /opt/python-deps -r /tmp/requirements.linux-demo.lock

FROM --platform=linux/amd64 python:3.14.6-slim-bookworm@sha256:f70215e5dbe2a47dee6d23f9c6d358bf3c148f59cce2fd165b61118e9d80f2bb
WORKDIR /opt/projectb
ENV PYTHONPATH=/opt/projectb/backend:/opt/python-deps \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOME=/nonexistent \
    PROJECTB_PROFILE=demo \
    PROJECTB_PROVIDER_ADAPTER=deterministic.mock \
    PROJECTB_EGRESS_POLICY=deny \
    PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring \
    PROJECTB_DATA_ROOT=/tmp/projectb-demo \
    PROJECTB_BIND_HOST=0.0.0.0 \
    PROJECTB_PORT=7860
COPY --from=python-deps /opt/python-deps /opt/python-deps
COPY backend /opt/projectb/backend
COPY --from=frontend-build /src/frontend/dist /opt/projectb/frontend_dist
COPY licenses/THIRD_PARTY_NOTICES.md /opt/projectb/licenses/THIRD_PARTY_NOTICES.md
COPY packaging/oci/sbom.spdx.json /opt/projectb/licenses/sbom.spdx.json
COPY packaging/oci/THIRD_PARTY_NOTICES.md /opt/projectb/licenses/OCI_THIRD_PARTY_NOTICES.md
COPY packaging/oci/requirements.linux-demo.lock /opt/projectb/licenses/requirements.linux-demo.lock
COPY frontend/package-lock.json /opt/projectb/licenses/frontend-package-lock.json
COPY docs/engineering/DEPENDENCY_BASELINE.md /opt/projectb/licenses/DEPENDENCY_BASELINE.md
COPY --chmod=0555 packaging/oci/entrypoint.sh /usr/local/bin/projectb-entrypoint
RUN mkdir -p /opt/projectb/licenses/debian-notices /tmp/projectb-demo \
    && cp -a /usr/share/doc/. /opt/projectb/licenses/debian-notices/ \
    && dpkg-query -W -f='${Package}\t${Version}\n' > /opt/projectb/licenses/debian-packages.tsv \
    && chmod -R a-w /opt/projectb/backend /opt/projectb/frontend_dist /opt/projectb/licenses \
    && chmod 1770 /tmp/projectb-demo \
    && chown 10001:10001 /tmp/projectb-demo \
    && python -c "import socket; assert hasattr(socket, 'getaddrinfo') and hasattr(socket, 'connect')"
# create_demo_app installs the Python socket.getaddrinfo/socket.connect guards.
USER 10001:10001
EXPOSE 7860
HEALTHCHECK --interval=10s --timeout=3s --start-period=20s --retries=6 CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:7860/api/settings', timeout=2)"
ENTRYPOINT ["/usr/local/bin/projectb-entrypoint"]
