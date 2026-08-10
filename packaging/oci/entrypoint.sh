#!/bin/sh
set -eu

: "${PROJECTB_PROFILE:?PROJECTB_PROFILE is required}"
: "${PROJECTB_PROVIDER_ADAPTER:?PROJECTB_PROVIDER_ADAPTER is required}"
: "${PROJECTB_EGRESS_POLICY:?PROJECTB_EGRESS_POLICY is required}"
: "${PYTHON_KEYRING_BACKEND:?PYTHON_KEYRING_BACKEND is required}"
: "${PROJECTB_DATA_ROOT:?PROJECTB_DATA_ROOT is required}"
: "${PROJECTB_PORT:?PROJECTB_PORT is required}"
[ "$#" -eq 0 ] || { echo oci_arguments_invalid >&2; exit 64; }
[ "$PROJECTB_PROFILE" = "demo" ] || { echo oci_profile_invalid >&2; exit 64; }
[ "$PROJECTB_PROVIDER_ADAPTER" = "deterministic.mock" ] || { echo oci_provider_invalid >&2; exit 64; }
[ "$PROJECTB_EGRESS_POLICY" = "deny" ] || { echo oci_egress_invalid >&2; exit 64; }
[ "$PYTHON_KEYRING_BACKEND" = "keyring.backends.null.Keyring" ] || { echo oci_keyring_invalid >&2; exit 64; }
[ "$PROJECTB_DATA_ROOT" = "/tmp/projectb-demo" ] || { echo oci_data_root_invalid >&2; exit 64; }
[ "${PROJECTB_BIND_HOST:-}" = "0.0.0.0" ] || { echo oci_bind_host_invalid >&2; exit 64; }
[ "$PROJECTB_PORT" = "7860" ] || { echo oci_port_invalid >&2; exit 64; }
[ "$(id -u)" = "10001" ] && [ "$(id -g)" = "10001" ] || { echo oci_user_invalid >&2; exit 64; }
mkdir -p "$PROJECTB_DATA_ROOT"

exec /usr/local/bin/python -c 'import os; from pathlib import Path; import uvicorn; from projectb.profiles.demo import create_demo_app; app = create_demo_app(session_root=Path(os.environ["PROJECTB_DATA_ROOT"]), static_dir=Path("/opt/projectb/frontend_dist"), environment=os.environ); uvicorn.run(app, host=os.environ.get("PROJECTB_BIND_HOST", "0.0.0.0"), port=int(os.environ["PROJECTB_PORT"]), proxy_headers=False, forwarded_allow_ips="")'
