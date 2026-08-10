# CI-01 Evidence

CI-01 is locally verified at the structural and test-suite level. Remote GitHub
Actions/GitLab execution remains `not_executed`. OCI runtime closure remains
`blocked_external_network` because DIST-02 cannot obtain the pinned base-image
manifests from `auth.docker.io`; this document makes no Docker or remote CI PASS
claim.

```json
{
  "task": "CI-01",
  "status": "in_progress",
  "verifier": {
    "status": "pass",
    "command": "python scripts/verify_ci_contract.py",
    "receipt": "CI_CONTRACT_PASS",
    "mappingSchema": "ci-contract-v1",
    "jobs": {
      "github": ["backend", "frontend", "oci-package", "scanner", "windows-package"],
      "gitlab": ["backend", "frontend", "oci-package", "unit-test"]
    }
  },
  "contractTests": {
    "status": "pass",
    "command": "python -m pytest backend/tests/contracts/test_ci_files.py -q",
    "receipt": "15 passed",
    "seed": "CI_SEED_CONTRACT_PASS"
  },
  "localSuites": {
    "backend": "TEST_ALL_PASS mode=backend; 269 passed",
    "frontend": "TEST_ALL_PASS mode=frontend; 60 passed",
    "credentialScan": "CREDENTIAL_SCAN_PASS files=508",
    "licenses": "LICENSE_VERIFICATION_PASS python=54 npm=166 direct_python=18 direct_npm=16"
  },
  "distribution": {
    "windows": {"status": "predecessor_local_pass", "runner": "not_executed", "evidence": "DIST-01_EVIDENCE.md"},
    "ociBuild": {
      "status": "blocked_external_network",
      "command": "docker build --platform linux/amd64 --file packaging/oci/Dockerfile --tag projectb-demo:local .",
      "engine": "29.1.2 linux/amd64",
      "blocker": "auth.docker.io anonymous-token timeout"
    },
    "ociRunAndSmoke": {"status": "not_executed"}
  },
  "remote": {"githubActions": "not_executed", "gitlab": "not_executed"},
  "publication": {"registryPush": "not_executed", "publicUrl": "waived", "deployment": "waived"}
}
```

The verifier found and the workflow edits closed two assembly drifts: backend
jobs now invoke `python scripts/test_all.py --backend` directly, with no
pre-feature empty-suite fallback, and every job has an explicit bounded
timeout. Action SHAs, container digests, push triggers, least permissions,
locked installs, Windows packaging, OCI inspection/smoke commands, and failure
propagation are checked structurally. Unknown jobs and bypass fields are
rejected with stable `CI_CONTRACT_RED` receipts.
