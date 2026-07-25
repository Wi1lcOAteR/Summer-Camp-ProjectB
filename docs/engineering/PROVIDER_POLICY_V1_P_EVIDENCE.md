# Provider Policy v1 P-Only Evidence

Status: **PASS - P-EVIDENCE planning input; no live API call authorized or claimed**

Verified `2026-07-25` (Asia/Shanghai) through the official OpenAI Developer Docs
MCP. Expires at the start of `2026-08-25` local time; P calls fail closed after
that point until this document and its verifier are refreshed from official
sources. No API key, request, account lookup, course material, or paid call was
used.

This snapshot supplements rather than rewrites the established 63-row evidence
ledger. The earlier `PROVIDER_POLICY_EVIDENCE.md` remains historical P/F research;
it does not authorize F, direct PDF/file input, hosted tools, or durable remote
objects in reduced v1.

| ID | Current v1 term | Official source | Verified consequence |
| --- | --- | --- | --- |
| `p-scope` | P sends only locally extracted, user-previewed text fragments; direct PDF/image/File/Vector Store and every hosted tool are excluded | ProjectB confirmed SPEC plus [Responses API reference](https://api.openai.com/v1/responses) | Request allowlist rejects `input_file`, `input_image`, `file_id`, `file_data`, `tools`, `previous_response_id`, `background:true`, and non-text content before network I/O. |
| `responses-shape` | `POST /v1/responses` supports `store`, `max_output_tokens`, text input, and structured text output | [OpenAI Responses OpenAPI](https://api.openai.com/v1/responses) | Adapter fixes `store:false`, `background:false`, `tools:[]`, `service_tier:default`, one request, 60-second timeout, zero automatic retries, and a strict Pydantic-derived JSON schema. |
| `retention` | API data is not used for training unless explicitly opted in; default abuse-monitoring logs may retain prompts/responses for up to 30 days; Responses with `store:false` avoid response application state, but prompt caching and safety exceptions remain distinct | [OpenAI data controls](https://developers.openai.com/api/docs/guides/your-data) | Every consent preview discloses non-training use, up-to-30-day abuse monitoring, possible encrypted prompt-cache state up to 24 hours, and that `store:false` is not a claim of ZDR. Background, audio, images/files, MCP, containers, and server compaction are unused. |
| `models` | `gpt-5.6-terra` balances intelligence/cost; `gpt-5.6-luna` targets cost-sensitive workloads; both support Responses and Structured Outputs, with 922,000 max input and 128,000 max output in the current snapshot | [Terra model](https://developers.openai.com/api/docs/models/gpt-5.6-terra), [Luna model](https://developers.openai.com/api/docs/models/gpt-5.6-luna) | Real provider is never selected by default. A profile must explicitly choose one allowlisted ID. ProjectB adds a conservative per-request ceiling of 20,000 input and 3,000 output tokens; configured caps may be lower and are consent-bound. |
| `pricing` | Standard per-million-token rates: Terra input `$2.50`, cache write `$3.125`, cached input `$0.25`, output `$15`; Luna input `$1`, cache write `$1.25`, cached input `$0.10`, output `$6`; eligible regional processing adds 10% | [OpenAI API pricing](https://developers.openai.com/api/docs/pricing) | Cost preview uses the worse of uncached-input or cache-write rate, the configured output cap, and a 10% regional reserve. At absolute ProjectB caps the ceilings are `$0.11825` Terra and `$0.04730` Luna. Changed/missing rates or arithmetic mismatch means zero network calls; there is no unrelated `$1` constant. |
| `structured-output` | Structured Outputs via `text.format` enforce a supplied JSON Schema; refusals are represented separately and model content can still be semantically wrong | [Structured model outputs](https://developers.openai.com/api/docs/guides/structured-outputs) | Adapter parses a strict candidate schema, handles refusal/incomplete/error explicitly, and keeps every candidate non-authoritative. It never retries malformed content into authority state. |
| `freshness` | API/model/pricing/data-control facts can change independently | the five official sources above | The policy fingerprint includes canonical evidence SHA-256, verification/expiry instants, allowlist, rates, caps, and request-field allowlist. Missing/stale/mismatched evidence returns `provider_unavailable` before reading a key or opening a socket. |

## Exact Cost Formula

For model profile `m`, configured input cap `I <= 20,000`, output cap
`O <= 3,000`, standard service tier, and regional reserve `R = 1.10`:

```text
C_max(m, I, O) = R * (I * max(input_rate_m, cache_write_rate_m)
                         + O * output_rate_m) / 1_000_000
```

The consent screen shows the selected model, exact fragments/locators/hashes,
`I`, `O`, the dated rates, and `C_max`. Usage below the caps may cost less; the
preview is an upper bound, not a quote or evidence of a charge.

## Exact Request Allowlist

The P-02 adapter may send only these top-level semantics: model, system
instruction, one user text input assembled from confirmed fragments,
`store:false`, `background:false`, `service_tier:default`, `reasoning.effort:low`,
`max_output_tokens`, strict `text.format`, empty tools, and a privacy-preserving
local safety identifier if the implementation can prove it contains no student
or material data. Every other optional API feature is absent. The response ID,
raw body, fragments, and model prose are not written to normal logs.

## Verification

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verify_provider_policy_v1.ps1
```

The verifier binds canonical document bytes and the required P-only terms. It
does not call OpenAI and does not claim model quality, account access, quota,
regional eligibility, actual retention controls, or spend.
