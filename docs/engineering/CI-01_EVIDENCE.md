# CI-01 Evidence

CI-01 is locally verified at the structural and test-suite level. Remote GitHub
Actions/GitLab execution remains `not_executed`, as required before authorization.
DIST-02's exact local image/run/smoke/browser gates are complete at `5145fea`;
this document does not turn those local receipts into a remote CI or publication
claim.

```json
{
  "task": "CI-01",
  "status": "ready_for_terminal_review",
  "implementationCommit": "pending_terminal_commit",
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
    "receipt": "21 passed",
    "seed": "CI_SEED_CONTRACT_PASS"
  },
  "localSuites": {
    "backend": "TEST_ALL_PASS mode=all; 277 passed",
    "frontend": "TEST_ALL_PASS mode=frontend; 60 passed",
    "credentialScan": "CREDENTIAL_SCAN_PASS files=514",
    "licenses": "LICENSE_VERIFICATION_PASS python=54 npm=166 direct_python=18 direct_npm=16"
  },
  "distribution": {
    "windows": {"status": "predecessor_local_pass", "runner": "not_executed", "evidence": "DIST-01_EVIDENCE.md"},
    "ociBuild": {
      "status": "predecessor_local_pass",
      "command": "docker build --platform linux/amd64 --file packaging/oci/Dockerfile --tag projectb-demo:local .",
      "engine": "29.1.2 linux/amd64",
      "image": "sha256:895b7df70ba3622c91d186c8856d9e97414a94bedc2e4d626791a7340d77d234",
      "evidence": "DIST-02_EVIDENCE.md"
    },
    "ociRunAndSmoke": {"status": "predecessor_local_pass", "receipt": "OCI_NETWORK_COUNT=0; OCI_SMOKE_PASS; DIST02_BROWSER_PASS"}
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
rejected with stable `CI_CONTRACT_RED` receipts. Negative tests additionally
reject GitLab job `rules`, GitHub step conditions, shell `if`/`case`/`until`,
uninvoked functions in both `name() {` and `function name {` forms, subshells,
brace groups, heredocs, command substitutions, command-shadowing functions,
GitLab `before_script`, wrapped lock/preflight commands, and indirect scanner,
Windows, or OCI commands. Canonical JSON SHA-256 digests bind each complete
reviewed job structure after semantic checks, so any unrecognized key, step,
script, order, wrapper, root variable, or stage drift fails closed. The stable mapping lists backend,
frontend, scanner, Windows, and OCI command groups.
