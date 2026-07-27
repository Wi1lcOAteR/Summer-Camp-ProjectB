# Bootstrap License Evidence

**Status:** VERIFIED INPUT / NOT PRODUCT EVIDENCE

**Observed:** 2026-07-27 (Asia/Shanghai)

This table fixes the exact license bytes that F-01A may copy into `licenses/bootstrap/`. The coordinator queried the official GitHub Contents and Git Refs APIs with no authentication, resolved each release tag to a commit, decoded the returned base64 content, and computed SHA-256 over those bytes. Direct PowerShell/curl raw downloads failed with local Schannel `SEC_E_NO_CREDENTIALS`, and a Python raw request timed out; those failed transports were not used as evidence.

| F-01A target | Project tag | Immutable commit and source | Git blob | Bytes | SHA-256 | License |
| --- | --- | --- | --- | ---: | --- | --- |
| `licenses/bootstrap/uv-LICENSE-APACHE` | uv `0.11.14` | `3fdfdc7d4a63c9f283eb751823b7628b13116684`; `https://raw.githubusercontent.com/astral-sh/uv/3fdfdc7d4a63c9f283eb751823b7628b13116684/LICENSE-APACHE` | `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64` | 11357 | `C71D239DF91726FC519C6EB72D318EC65820627232B2F796219E87DCF35D0AB4` | Apache-2.0 |
| `licenses/bootstrap/uv-LICENSE-MIT` | uv `0.11.14` | `3fdfdc7d4a63c9f283eb751823b7628b13116684`; `https://raw.githubusercontent.com/astral-sh/uv/3fdfdc7d4a63c9f283eb751823b7628b13116684/LICENSE-MIT` | `014835144877ea9c926d027ece3e1a26290cf481` | 1077 | `860E3D7A86B84E6A7012C7A635FC64DF475CEBC6CCE34DFEB73A5982EC58176C` | MIT |
| `licenses/bootstrap/cpython-LICENSE` | CPython `v3.14.6` | `c63aec69bd59c55314c06c23f4c22c03de76fe45`; `https://raw.githubusercontent.com/python/cpython/c63aec69bd59c55314c06c23f4c22c03de76fe45/LICENSE` | `20cf39097c68baa17cc566b64e76d34ebf034044` | 13804 | `B0E25A78CFFB43F4D92DE8B61CCFA1F1F98ECBC22330B54B5251E7B6BA010231` | PSF-2.0 plus bundled notices |
| `licenses/bootstrap/node-LICENSE` | Node.js `v24.18.0` | `20da4aeadabc5b0a01e3fcf520f91df8285c68a2`; `https://raw.githubusercontent.com/nodejs/node/20da4aeadabc5b0a01e3fcf520f91df8285c68a2/LICENSE` | `2842efa1288eef1de3a6778b5dd3519bc903308d` | 157606 | `148EACF7863EF4329224A29398623077200A27194AA075569FAF4A0A85566CA5` | MIT plus bundled notices |
| `licenses/bootstrap/npm-LICENSE` | npm CLI `v11.16.0` | `960135ad6e26b2b656e23848690c9cfe3cb3783b`; `https://raw.githubusercontent.com/npm/cli/960135ad6e26b2b656e23848690c9cfe3cb3783b/LICENSE` | `0b6c2287459632e4aaf63bd7d53eb9ba054b57ea` | 9742 | `7610D223851F421D315DF5E77974F1C68A04B97E02060E5BBBCF13D95E3CA257` | Artistic-2.0 |

F-01A must fetch only the immutable commit URLs, verify byte count and SHA-256 before copying, and fail closed on any mismatch. The release artifact hashes in `DEPENDENCY_BASELINE.md` remain separate mandatory checks.
