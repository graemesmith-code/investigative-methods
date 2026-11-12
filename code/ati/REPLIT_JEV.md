# Optional Replit-managed Jev boundary

`jev_transport.py` adds an opt-in `JevAdapter`; it is not enabled by any existing
runner. `pipeline.py`, its native TypeSafe payloads, pinned `jev-1.13.0` model,
pricing, ledger, and continuation safeguards are unchanged. Coverage screening
currently uses that direct runner (`match_coverage.py`). The recent Alberta
gap-ranking script also delegates to its direct client. No managed route was
present in these paths at base commit
`218de208b504372e06f73abae79de1e2e21d25a1`.

## Exact configuration contract

Construct `JevAdapter(route='replit-openrouter', send=send,
connection_id='non-secret-app-connection-label')` explicitly. There is no
environment-variable discovery, default endpoint, guessed managed key, or
automatic switch when a direct key is absent.

1. In the target Replit app, enable **OpenRouter (Replit managed)** using Replit
   Agent. Ask it to use Jev via AI Integrations. This repository does not provision
   a connection or infer its endpoint, credential names, headers, or SDK.
2. Supply `send(body) -> dict` from the actual generated workspace integration.
   It must use that app's verified Replit-managed connection, preserve Replit's
   configured privacy defaults, perform one non-streaming request, return the
   decoded provider response, and propagate errors without retries/fallbacks.
   Disable SDK retries and credential-bearing redirects in that binding.
   A personal OpenRouter key is not a Replit-managed connection.
3. Supply a workspace-verified OpenRouter chat request with explicit `model`
   (Replit documents `jev-latest`) and nonempty `messages`. Do not pass native
   TypeSafe `state/questions`. The official Replit page does not document how
   native Jev questions map onto chat, so this adapter deliberately does not
   invent a translation, structured-output schema, or score parser.
4. Call `adapter.call(body, provenance={...})`, including source identifiers,
   source hashes, run identifier and prompt version as appropriate. Persist the
   entire returned envelope. `transport` contains route, gateway provider,
   credential source, connection identifier, requested model, provider-returned
   `model`, request hash and route-specific cache key. `response` remains intact,
   including usage and any upstream provider fields. The returned model is what
   the provider reports; it is not proof of an underlying model version if the
   provider itself returns an alias. Missing model identifiers fail closed.
5. Use the returned request identity for a separate managed-route cache and
   ledger. Reserve a verified managed-route cost bound **before** calling this
   boundary. Do not insert these responses into the ATI direct ledger: its
   validators, fixed prices and budget assumptions do not cover OpenRouter.
   Reconcile cost and validate the response against the task's reviewed schema
   before accepting scores. This adapter is a transport/provenance boundary,
   not a new paid-run entry point or spending authorization.

For direct use, `route='typesafe'` accepts native requests unchanged; bind
`send=lambda body: existing_transport('jev', body)` and retain the existing
validation/accounting. Existing callers do not need to adopt the adapter.

## Verified sources and limits

Read on 2026-10-07:

- [Replit AI Integrations](https://docs.replit.com/references/integrations/replit-ai-integrations):
  `jev-latest` through OpenRouter; managed credentials on paid plans; public API
  prices billed to Replit credits; plan-specific OpenRouter privacy defaults.
  It describes Agent provisioning but supplies no reproducible managed OpenRouter
  authentication or native Jev-to-chat mapping contract.
- [OpenRouter quickstart](https://openrouter.ai/docs/quickstart): standard chat
  completions and OpenAI-compatible clients. Its public endpoint and personal
  bearer-key examples do not establish Replit-managed workspace authentication.

Work stops at this boundary until the target app's generated integration can be
inspected. No model inference calls were made. Fixtures are synthetic transport
examples, not evidence of a functioning live Jev chat schema.

## Offline verification

`python -m unittest discover -s code/ati -v`

New tests block socket connections and check route/model/connection cache
separation, direct pass-through, response model recording, source provenance,
missing configuration, rejected native/chat mixing, and no retry/fallback.
