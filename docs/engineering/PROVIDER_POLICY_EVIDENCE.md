# Provider Policy Evidence

Status: **PASS - G-02B pre-implementation evidence committed; live F remains disabled**

Verification date: `2026-07-21` (Asia/Shanghai). Every row was fetched through the official OpenAI Developer Docs MCP. No API key, request body, course material, or paid API call was used.

`verified` means the current fact is established, including an official non-guarantee that maps to a deterministic SPEC fail-closed state. It does not mean a live adapter or account capability was tested. Runtime mode F remains `source_disabled` until X2-03 deterministic contract tests and the separately authorized INT-01 live evidence succeed.

| ID | Item | Version/term | Source URL | License/authority | Verified | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| responses | Responses application state | /v1/responses; store:false disables Responses application state; background mode stores data for roughly 10 minutes | https://developers.openai.com/api/docs/guides/your-data#storage-requirements-and-retention-controls-per-endpoint | OpenAI Developer Docs data-controls table | 2026-07-21 | verified | API data is not used for training without explicit consent. store:false does not remove abuse-monitoring, safety-review, or cache semantics and is not ZDR. Background mode and non-essential hosted state are disabled. |
| abuse-monitoring | Abuse monitoring | default logs may contain prompts, responses, and classifier metadata for up to 30 days, subject to stated exceptions | https://developers.openai.com/api/docs/guides/your-data#data-retention-controls-for-abuse-monitoring | OpenAI Developer Docs data controls | 2026-07-21 | verified | Must be presented in each P/F policy snapshot and cannot be replaced by a training-use statement. |
| prompt-cache | Prompt cache | encrypted cache state may remain on local GPU machines up to 24 hours; model caveats apply | https://developers.openai.com/api/docs/guides/your-data#storage-requirements-and-retention-controls-per-endpoint | OpenAI Developer Docs data controls | 2026-07-21 | verified | store:false does not remove non-ZDR prompt-cache behavior. |
| file-review | Image/file safety review | submitted image/file inputs are scanned; a potential CSAM classifier hit may retain input for manual review even with ZDR/MAM/Eyes Off | https://developers.openai.com/api/docs/guides/your-data#image-and-file-inputs | OpenAI Developer Docs data controls | 2026-07-21 | verified | This exception is displayed before consent. |
| files | Files endpoint | /v1/files state retained until deleted; not ZDR eligible | https://developers.openai.com/api/docs/guides/your-data#storage-requirements-and-retention-controls-per-endpoint | OpenAI Developer Docs endpoint table | 2026-07-21 | verified | expires_after or explicit deletion is required. Deleting a base File removes it from all Vector Stores, so local ownership and association checks precede deletion. |
| vector-stores | Vector Stores endpoint | /v1/vector_stores state retained until deleted; not ZDR eligible; deleted Vector Store objects may take up to 30 days to be removed from OpenAI servers | https://developers.openai.com/api/docs/guides/your-data#storage-requirements-and-retention-controls-per-endpoint | OpenAI Developer Docs endpoint table | 2026-07-21 | verified | Each course/profile/config uses a separate store. Expiry does not substitute for explicit base File reconciliation. Delete acceptance is not represented as immediate physical purge; the UI must present the documented server-removal window. |
| deletion-expiry | Layered deletion and expiry | association, File, and Vector Store delete endpoints are distinct; association deletion may be eventually consistent | https://developers.openai.com/api/reference/resources/vector_stores/subresources/files/methods/delete | OpenAI API reference | 2026-07-21 | verified | Removing an association does not delete its base File. Local scope is revoked before the remote request. Unknown request/reconciliation completion becomes delete_incomplete; a confirmed Vector Store delete response is recorded as accepted and uses the separate vector-stores retention disclosure, never as instantaneous purge or exactly-once deletion. |
| region | Regional storage and processing | regional storage does not imply regional processing; non-US use requires stated retention controls and endpoint/model eligibility | https://developers.openai.com/api/docs/guides/your-data#data-residency-controls | OpenAI Developer Docs residency table | 2026-07-21 | verified | Regional processing adds a 10 percent model-price uplift for this reference model. File Search processing support remains profile/account dependent and fails closed when not proven. |
| model-reference | Bounded evidence reference profile | gpt-5.4-mini-2026-03-17; Responses; 272000 max input; 128000 max output; image, Structured Outputs, File Search, file upload | https://developers.openai.com/api/docs/models/gpt-5.4-mini | OpenAI model catalog | 2026-07-21 | verified | This exact snapshot is used only for evidence arithmetic and adapter contract fixtures. It is not a silent runtime default; the user config must select a supported profile explicitly. |
| p-input-file | P direct PDF input | input_file provides extracted text and page images to a vision-capable model; file_data/base64 avoids a persistent Files object | https://developers.openai.com/api/docs/guides/file-inputs#how-it-works | OpenAI Developer Docs file-input guide | 2026-07-21 | verified | P remains subject to local page/region locator validation and a fresh consent record. Capability evidence does not prove explanation quality. |
| input-token-count | Preflight token count | POST /v1/responses/input_tokens accepts the same text, image, PDF, tool, and schema inputs and returns exact input_tokens | https://developers.openai.com/api/docs/guides/token-counting | OpenAI Developer Docs token-counting guide | 2026-07-21 | verified | P/F must count before generation and fail before the paid request when the count, price snapshot, or hard bound is unavailable. A duplicate full input-charge reserve is included because no separate count-endpoint price is listed. |
| f-filter-results | F filter and result primitives | vector_store.file attributes up to 16 keys; in metadata filter; include file_search_call.results; results/citations expose File IDs | https://developers.openai.com/api/docs/guides/tools-file-search#metadata-filtering | OpenAI Developer Docs File Search and Retrieval guides | 2026-07-21 | verified | The adapter must request included results and post-validate every File ID against the local allowlist. Native citations do not prove PDF page/visual locators. |
| pricing | Bounded P/F preflight | gpt-5.4-mini standard input US$0.75/M, output US$4.50/M; File Search US$0.0025/call and US$0.10/GiB-day; regional multiplier 1.10 | https://developers.openai.com/api/docs/pricing | OpenAI Developer Docs pricing | 2026-07-21 | verified | With I=20000, O=3000, one File Search call, one GiB-day reserve, and a duplicate input-count reserve, ceiling is US$0.15035. Any missing/changed term or total over US$1.00 makes provider calls zero. |
| pf-unsupported | F documented boundary and runtime gate | filter-list maximum, native page locator, create idempotency, exactly-once upload/delete, immediate deletion, account region/limit/storage state are not guaranteed | https://developers.openai.com/api/reference/overview#supplying-your-own-request-id-with-x-client-request-id | OpenAI docs plus ProjectB fail-closed contract | 2026-07-21 | verified | X-Client-Request-Id is tracing, not deduplication. Use no automatic create retry, local idempotency, duplicate isolation/reconciliation, delete_incomplete, and source_disabled when any required capability is unproven. |

## Cost Bound

For the exact evidence reference profile, use standard service rates and reserve the regional uplift even when the selected account later uses US processing:

```text
C_count_reserve = 1.10 * (I * 0.75 / 1_000_000)
C_generation    = 1.10 * ((I * 0.75 + O * 4.50) / 1_000_000)
C_file_search   = 0.0025 * N_file_search_calls
C_storage       = 0.10 * indexed_GiB_days
C_total         = C_count_reserve + C_generation + C_file_search + C_storage
```

For the AC-48 evidence envelope, `I <= 20,000`, `O <= 3,000`, `N_file_search_calls <= 1`, and `indexed_GiB_days <= 1`, yielding:

```text
0.01650 + 0.03135 + 0.00250 + 0.10000 = US$0.15035
```

The implementation stores the dated model/price/service-tier/region snapshot and exact count with the consent record. It must not rely on the account-wide free storage allowance. A wider file scope, extra tool call, unknown retrieval result size, changed model/price, or unavailable token count fails before generation. This is an offline arithmetic proof, not evidence of an actual charge or successful request.

## P and F Enforcement

- P may use direct Base64 PDF input after local validation and consent. It still requires schema validation, local SourceLocator proof, a 20k input cap, timeout, output cap, and the US$1 preflight.
- F has documented attributes/filter/result/delete primitives, but starts `source_disabled`. X2-03 may enable only the exact tested capability snapshot and scope sizes; every returned File ID is checked locally.
- The official OpenAPI does not document provider idempotency for Responses, Files, Vector Stores, or associations. Create operations are not automatically retried; recovery enumerates and reconciles remote objects.
- A deleted association may briefly remain searchable. The allowlist is revoked locally first, then remote cleanup is reconciled. Uncertain cleanup remains visible as delete_incomplete.
- A successful Vector Store delete request means deletion was accepted, not that all server copies disappeared immediately. Local use remains disabled, and status/help text preserves the documented maximum 30-day server-removal window.
- No live account capability, regional eligibility, rate limit, provider quality, or actual spend is claimed here. Those require the user's later authorization and INT-01.

## Gate

G-02B passed in commit `5ac9d47ddda845ed78f1758326fb547610274f4c`. The evidence is sufficient to implement without guessing because positive primitives and negative guarantees both map to deterministic behavior. This PASS does not enable F, authorize a provider call, or claim AC-48 live evidence.
