# Resume AI Service — Postman

Import **`Resume_AI_Service.postman_collection.json`** into Postman (File → Import).

## Variables

| Variable    | Description |
|------------|-------------|
| `baseUrl`  | API base with **no** trailing slash (e.g. `https://u4so6v3jsj.execute-api.us-east-1.amazonaws.com` from `sam deploy` output, or `http://127.0.0.1:8080` locally). |
| `apiKey`   | Same value as **`API_KEY`** / SAM parameter **ApiKey** — sent as **`X-API-Key`**. |
| `userId`   | User UUID string for list/create examples (must match a `users.uuid` in Postgres when using shared DB). |
| `resumeId` | Set after **Resume → Create resume** from the response `id`, or paste manually for get/update/delete. |

## Auth

- **Root** and **Health** requests use **no auth** (public).
- **Resume** and **AI** folders inherit collection auth: **API Key** in header **`X-API-Key`** = `{{apiKey}}`.

## Multipart requests

- **AI → Parse resume (multipart)** and **Enhance photo**: choose a local file for the `file` field in the Body tab.

## OpenAPI

When the service is running, interactive docs: **`GET {{baseUrl}}/docs`** (Swagger UI).

## Related docs

- `docs/backend/apis/29_RESUME_AI_REST_SERVICE.md` — full REST reference and integration notes.
