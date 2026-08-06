# Third-Party Notices

ProjectB uses the pinned Python and npm packages recorded in `pyproject.toml`,
`frontend/package-lock.json`, and the reviewed closure in
`docs/engineering/DEPENDENCY_BASELINE.md`. Those lock files are the canonical
version inventory; this notice records the direct package names and the
obligations that must remain present in a distributed artifact.

The verified closure is 54 Python packages and 166 npm packages. Its exact
versions, integrity values, and reviewed license terms are bound to the
canonical-LF hashes of the two production lock files by
`scripts/verify_licenses.py`; an unreviewed package, incompatible term, or
lock change fails that gate.

## Python Direct Packages

FastAPI 0.139.2; Uvicorn 0.51.0; Pydantic 2.13.4; HTTPX 0.28.1; HTTPX2
2.7.0; OpenAI 2.46.0; pypdf 6.14.2; pypdfium2 5.12.1; Pillow 12.3.0;
keyring 25.7.0; tzdata 2026.3; python-multipart 0.0.32; psutil 7.2.2;
pytest 9.1.1; Ruff 0.15.22; mypy 2.3.0; types-psutil 7.2.2.20260518; and
PyInstaller 6.21.0. The closure includes MIT, Apache-2.0, BSD variants,
MPL-2.0, PSF-2.0, MIT-CMU, and the PyInstaller bootloader exception. A
distribution must retain the pypdfium2/PDFium notices, MPL covered-file
obligations, setuptools vendor notices, and the PyInstaller COPYING text.

## npm Direct Packages

React 19.2.7; react-dom 19.2.7; lucide-react 1.25.0; Vite 8.1.5;
@vitejs/plugin-react 6.0.3; Vitest 4.1.10; TypeScript 7.0.2; jsdom 29.1.1;
@testing-library/dom 10.4.1; @testing-library/react 16.3.2;
@testing-library/user-event 14.6.1; @playwright/test 1.61.1;
@axe-core/playwright 4.12.1; @types/node 24.13.3; @types/react 19.2.17;
and @types/react-dom 19.2.3. The locked closure uses MIT, Apache-2.0,
MPL-2.0, ISC, BSD, MIT-0, 0BSD, BlueOak-1.0.0, and CC0-1.0. Retain the
Playwright, axe, TypeScript, Vite, Lucide, Node, and npm notices in the final
distribution.

## Complete lock closures

The following machine-generated inventory is the notice coverage for every package in the production Windows, Linux CI, Linux demo, and npm closures. The verifier checks each lock set, version, license term, and closure digest; these rows are intentionally explicit so a missing notice cannot pass silently.

| ecosystem | package | version | license |
| --- | --- | --- | --- |
| npm | @asamuzakjp/css-color | 5.1.11 | MIT |
| npm | @asamuzakjp/dom-selector | 7.1.1 | MIT |
| npm | @asamuzakjp/generational-cache | 1.0.1 | MIT |
| npm | @asamuzakjp/nwsapi | 2.3.9 | MIT |
| npm | @axe-core/playwright | 4.12.1 | MPL-2.0 |
| npm | @babel/code-frame | 7.29.7 | MIT |
| npm | @babel/helper-validator-identifier | 7.29.7 | MIT |
| npm | @babel/runtime | 7.29.7 | MIT |
| npm | @bramus/specificity | 2.4.2 | MIT |
| npm | @csstools/color-helpers | 6.1.0 | MIT-0 |
| npm | @csstools/css-calc | 3.2.1 | MIT |
| npm | @csstools/css-color-parser | 4.1.9 | MIT |
| npm | @csstools/css-parser-algorithms | 4.0.0 | MIT |
| npm | @csstools/css-syntax-patches-for-csstree | 1.1.6 | MIT-0 |
| npm | @csstools/css-tokenizer | 4.0.0 | MIT |
| npm | @emnapi/core | 1.11.1 | MIT |
| npm | @emnapi/runtime | 1.11.1 | MIT |
| npm | @emnapi/wasi-threads | 1.2.2 | MIT |
| npm | @exodus/bytes | 1.15.1 | MIT |
| npm | @jridgewell/sourcemap-codec | 1.5.5 | MIT |
| npm | @napi-rs/wasm-runtime | 1.1.6 | MIT |
| npm | @oxc-project/types | 0.139.0 | MIT |
| npm | @playwright/test | 1.61.1 | Apache-2.0 |
| npm | @rolldown/binding-android-arm64 | 1.1.5 | MIT |
| npm | @rolldown/binding-darwin-arm64 | 1.1.5 | MIT |
| npm | @rolldown/binding-darwin-x64 | 1.1.5 | MIT |
| npm | @rolldown/binding-freebsd-x64 | 1.1.5 | MIT |
| npm | @rolldown/binding-linux-arm-gnueabihf | 1.1.5 | MIT |
| npm | @rolldown/binding-linux-arm64-gnu | 1.1.5 | MIT |
| npm | @rolldown/binding-linux-arm64-musl | 1.1.5 | MIT |
| npm | @rolldown/binding-linux-ppc64-gnu | 1.1.5 | MIT |
| npm | @rolldown/binding-linux-s390x-gnu | 1.1.5 | MIT |
| npm | @rolldown/binding-linux-x64-gnu | 1.1.5 | MIT |
| npm | @rolldown/binding-linux-x64-musl | 1.1.5 | MIT |
| npm | @rolldown/binding-openharmony-arm64 | 1.1.5 | MIT |
| npm | @rolldown/binding-wasm32-wasi | 1.1.5 | MIT |
| npm | @rolldown/binding-win32-arm64-msvc | 1.1.5 | MIT |
| npm | @rolldown/binding-win32-x64-msvc | 1.1.5 | MIT |
| npm | @rolldown/pluginutils | 1.0.1 | MIT |
| npm | @standard-schema/spec | 1.1.0 | MIT |
| npm | @testing-library/dom | 10.4.1 | MIT |
| npm | @testing-library/react | 16.3.2 | MIT |
| npm | @testing-library/user-event | 14.6.1 | MIT |
| npm | @tybys/wasm-util | 0.10.3 | MIT |
| npm | @types/aria-query | 5.0.4 | MIT |
| npm | @types/chai | 5.2.3 | MIT |
| npm | @types/deep-eql | 4.0.2 | MIT |
| npm | @types/estree | 1.0.9 | MIT |
| npm | @types/node | 24.13.3 | MIT |
| npm | @types/react | 19.2.17 | MIT |
| npm | @types/react-dom | 19.2.3 | MIT |
| npm | @typescript/typescript-aix-ppc64 | 7.0.2 | Apache-2.0 |
| npm | @typescript/typescript-darwin-arm64 | 7.0.2 | Apache-2.0 |
| npm | @typescript/typescript-darwin-x64 | 7.0.2 | Apache-2.0 |
| npm | @typescript/typescript-freebsd-arm64 | 7.0.2 | Apache-2.0 |
| npm | @typescript/typescript-freebsd-x64 | 7.0.2 | Apache-2.0 |
| npm | @typescript/typescript-linux-arm | 7.0.2 | Apache-2.0 |
| npm | @typescript/typescript-linux-arm64 | 7.0.2 | Apache-2.0 |
| npm | @typescript/typescript-linux-loong64 | 7.0.2 | Apache-2.0 |
| npm | @typescript/typescript-linux-mips64el | 7.0.2 | Apache-2.0 |
| npm | @typescript/typescript-linux-ppc64 | 7.0.2 | Apache-2.0 |
| npm | @typescript/typescript-linux-riscv64 | 7.0.2 | Apache-2.0 |
| npm | @typescript/typescript-linux-s390x | 7.0.2 | Apache-2.0 |
| npm | @typescript/typescript-linux-x64 | 7.0.2 | Apache-2.0 |
| npm | @typescript/typescript-netbsd-arm64 | 7.0.2 | Apache-2.0 |
| npm | @typescript/typescript-netbsd-x64 | 7.0.2 | Apache-2.0 |
| npm | @typescript/typescript-openbsd-arm64 | 7.0.2 | Apache-2.0 |
| npm | @typescript/typescript-openbsd-x64 | 7.0.2 | Apache-2.0 |
| npm | @typescript/typescript-sunos-x64 | 7.0.2 | Apache-2.0 |
| npm | @typescript/typescript-win32-arm64 | 7.0.2 | Apache-2.0 |
| npm | @typescript/typescript-win32-x64 | 7.0.2 | Apache-2.0 |
| npm | @vitejs/plugin-react | 6.0.3 | MIT |
| npm | @vitest/expect | 4.1.10 | MIT |
| npm | @vitest/mocker | 4.1.10 | MIT |
| npm | @vitest/pretty-format | 4.1.10 | MIT |
| npm | @vitest/runner | 4.1.10 | MIT |
| npm | @vitest/snapshot | 4.1.10 | MIT |
| npm | @vitest/spy | 4.1.10 | MIT |
| npm | @vitest/utils | 4.1.10 | MIT |
| npm | ansi-regex | 5.0.1 | MIT |
| npm | ansi-styles | 5.2.0 | MIT |
| npm | aria-query | 5.3.0 | Apache-2.0 |
| npm | assertion-error | 2.0.1 | MIT |
| npm | axe-core | 4.12.1 | MPL-2.0 |
| npm | bidi-js | 1.0.3 | MIT |
| npm | chai | 6.2.2 | MIT |
| npm | convert-source-map | 2.0.0 | MIT |
| npm | css-tree | 3.2.1 | MIT |
| npm | csstype | 3.2.3 | MIT |
| npm | data-urls | 7.0.0 | MIT |
| npm | decimal.js | 10.6.0 | MIT |
| npm | dequal | 2.0.3 | MIT |
| npm | detect-libc | 2.1.2 | Apache-2.0 |
| npm | dom-accessibility-api | 0.5.16 | MIT |
| npm | entities | 8.0.0 | BSD-2-Clause |
| npm | es-module-lexer | 2.3.1 | MIT |
| npm | estree-walker | 3.0.3 | MIT |
| npm | expect-type | 1.4.0 | Apache-2.0 |
| npm | fdir | 6.5.0 | MIT |
| npm | fsevents | 2.3.2 | MIT |
| npm | html-encoding-sniffer | 6.0.0 | MIT |
| npm | is-potential-custom-element-name | 1.0.1 | MIT |
| npm | js-tokens | 4.0.0 | MIT |
| npm | jsdom | 29.1.1 | MIT |
| npm | lightningcss | 1.33.0 | MPL-2.0 |
| npm | lightningcss-android-arm64 | 1.33.0 | MPL-2.0 |
| npm | lightningcss-darwin-arm64 | 1.33.0 | MPL-2.0 |
| npm | lightningcss-darwin-x64 | 1.33.0 | MPL-2.0 |
| npm | lightningcss-freebsd-x64 | 1.33.0 | MPL-2.0 |
| npm | lightningcss-linux-arm-gnueabihf | 1.33.0 | MPL-2.0 |
| npm | lightningcss-linux-arm64-gnu | 1.33.0 | MPL-2.0 |
| npm | lightningcss-linux-arm64-musl | 1.33.0 | MPL-2.0 |
| npm | lightningcss-linux-x64-gnu | 1.33.0 | MPL-2.0 |
| npm | lightningcss-linux-x64-musl | 1.33.0 | MPL-2.0 |
| npm | lightningcss-win32-arm64-msvc | 1.33.0 | MPL-2.0 |
| npm | lightningcss-win32-x64-msvc | 1.33.0 | MPL-2.0 |
| npm | lru-cache | 11.5.2 | BlueOak-1.0.0 |
| npm | lucide-react | 1.25.0 | ISC |
| npm | lz-string | 1.5.0 | MIT |
| npm | magic-string | 0.30.21 | MIT |
| npm | mdn-data | 2.27.1 | CC0-1.0 |
| npm | nanoid | 3.3.16 | MIT |
| npm | obug | 2.1.4 | MIT |
| npm | parse5 | 8.0.1 | MIT |
| npm | pathe | 2.0.3 | MIT |
| npm | picocolors | 1.1.1 | ISC |
| npm | picomatch | 4.0.5 | MIT |
| npm | playwright | 1.61.1 | Apache-2.0 |
| npm | playwright-core | 1.61.1 | Apache-2.0 |
| npm | postcss | 8.5.25 | MIT |
| npm | pretty-format | 27.5.1 | MIT |
| npm | punycode | 2.3.1 | MIT |
| npm | react | 19.2.7 | MIT |
| npm | react-dom | 19.2.7 | MIT |
| npm | react-is | 17.0.2 | MIT |
| npm | require-from-string | 2.0.2 | MIT |
| npm | rolldown | 1.1.5 | MIT |
| npm | saxes | 6.0.0 | ISC |
| npm | scheduler | 0.27.0 | MIT |
| npm | siginfo | 2.0.0 | ISC |
| npm | source-map-js | 1.2.1 | BSD-3-Clause |
| npm | stackback | 0.0.2 | MIT |
| npm | std-env | 4.2.0 | MIT |
| npm | symbol-tree | 3.2.4 | MIT |
| npm | tinybench | 2.9.0 | MIT |
| npm | tinyexec | 1.2.4 | MIT |
| npm | tinyglobby | 0.2.17 | MIT |
| npm | tinyrainbow | 3.1.0 | MIT |
| npm | tldts | 7.4.9 | MIT |
| npm | tldts-core | 7.4.9 | MIT |
| npm | tough-cookie | 6.0.2 | BSD-3-Clause |
| npm | tr46 | 6.0.0 | MIT |
| npm | tslib | 2.8.1 | 0BSD |
| npm | typescript | 7.0.2 | Apache-2.0 |
| npm | undici | 7.29.0 | MIT |
| npm | undici-types | 7.18.2 | MIT |
| npm | vite | 8.1.5 | MIT |
| npm | vite/node_modules/fsevents | 2.3.3 | MIT |
| npm | vitest | 4.1.10 | MIT |
| npm | w3c-xmlserializer | 5.0.0 | MIT |
| npm | webidl-conversions | 8.0.1 | BSD-2-Clause |
| npm | whatwg-mimetype | 5.0.0 | MIT |
| npm | whatwg-url | 16.0.1 | MIT |
| npm | why-is-node-running | 2.3.0 | MIT |
| npm | xml-name-validator | 5.0.0 | Apache-2.0 |
| npm | xmlchars | 2.2.0 | MIT |
| python | altgraph | 0.17.5 | MIT |
| python | annotated-doc | 0.0.4 | MIT |
| python | annotated-types | 0.7.0 | MIT |
| python | anyio | 4.14.2 | MIT |
| python | ast-serialize | 0.6.0 | MIT |
| python | certifi | 2026.6.17 | MPL-2.0 |
| python | click | 8.4.2 | BSD-3-Clause |
| python | colorama | 0.4.6 | BSD-3-Clause |
| python | distro | 1.9.0 | Apache-2.0 |
| python | fastapi | 0.139.2 | MIT |
| python | h11 | 0.16.0 | MIT |
| python | httpcore | 1.0.9 | BSD-3-Clause |
| python | httpcore2 | 2.7.0 | BSD-3-Clause |
| python | httpx | 0.28.1 | BSD-3-Clause |
| python | httpx2 | 2.7.0 | BSD-3-Clause |
| python | idna | 3.18 | BSD-3-Clause |
| python | iniconfig | 2.3.0 | MIT |
| python | jaraco-classes | 3.4.0 | MIT |
| python | jaraco-context | 6.1.2 | MIT |
| python | jaraco-functools | 4.6.0 | MIT |
| python | jiter | 0.16.0 | MIT |
| python | keyring | 25.7.0 | MIT |
| python | librt | 0.13.0 | MIT |
| python | more-itertools | 11.1.0 | MIT |
| python | mypy | 2.3.0 | MIT |
| python | mypy-extensions | 1.1.0 | MIT |
| python | openai | 2.46.0 | Apache-2.0 |
| python | packaging | 26.2 | Apache-2.0 OR BSD-2-Clause |
| python | pathspec | 1.1.1 | MPL-2.0 |
| python | pefile | 2024.8.26 | MIT |
| python | pillow | 12.3.0 | MIT-CMU |
| python | pluggy | 1.6.0 | MIT |
| python | psutil | 7.2.2 | BSD-3-Clause |
| python | pydantic | 2.13.4 | MIT |
| python | pydantic-core | 2.46.4 | MIT |
| python | pygments | 2.20.0 | BSD-2-Clause |
| python | pyinstaller | 6.21.0 | GPL-2.0-or-later WITH Bootloader-exception |
| python | pyinstaller-hooks-contrib | 2026.6 | GPL-2.0-or-later standard hooks; Apache-2.0 runtime hooks |
| python | pypdf | 6.14.2 | BSD-3-Clause |
| python | pypdfium2 | 5.12.1 | BSD-3-Clause plus Apache-2.0 and dependency notices including CC-BY-4.0 |
| python | pytest | 9.1.1 | MIT |
| python | python-multipart | 0.0.32 | Apache-2.0 |
| python | pywin32-ctypes | 0.2.3 | BSD-3-Clause |
| python | ruff | 0.15.22 | MIT |
| python | setuptools | 83.0.0 | MIT plus bundled vendor notices |
| python | sniffio | 1.3.1 | MIT OR Apache-2.0 |
| python | starlette | 1.3.1 | BSD-3-Clause |
| python | tqdm | 4.69.0 | MPL-2.0 AND MIT |
| python | truststore | 0.10.4 | MIT |
| python | types-psutil | 7.2.2.20260518 | Apache-2.0 |
| python | typing-extensions | 4.16.0 | PSF-2.0 |
| python | typing-inspection | 0.4.2 | MIT |
| python | tzdata | 2026.3 | Apache-2.0 |
| python | uvicorn | 0.51.0 | BSD-3-Clause |

## Bootstrap Toolchain Notices

The exact upstream texts for uv (Apache-2.0 or MIT), CPython (PSF-2.0), Node
(MIT), and npm (Artistic-2.0) are preserved under `licenses/bootstrap/`:
`uv-LICENSE-APACHE`, `uv-LICENSE-MIT`, `cpython-LICENSE`, `node-LICENSE`, and
`npm-LICENSE`. Their immutable provenance and byte hashes are in
`docs/engineering/BOOTSTRAP_LICENSE_EVIDENCE.md`.
