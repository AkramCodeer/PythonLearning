# Large-file analysis — infra setup (P2/P3)

The code for large-file analysis (signed PUT direct-to-GCS upload + DuckDB httpfs in the sandbox) is in
place. These **one-time infra steps** are required before it works end to end.

## 1. Sandbox image — new Python deps
`sandboxService/requirements.txt` added `duckdb`, `statsmodels` (and earlier `seaborn`/`reportlab` etc.).
Rebuild the sandbox:
```bash
cd ../sandboxService
pip install -r requirements.txt          # local venv
# or rebuild + redeploy the Cloud Run image
```

## 2. Reports/uploads bucket
Set `REPORT_GCS_BUCKET` (the same bucket the BigQuery report path uses is fine). Uploaded files land
under `gs://<bucket>/<REPORT_GCS_PREFIX>/uploads/<uuid>/<name>`.

The **agent service SA** (the one whose key is `report.gcs.credentials-path`, or the main
`services.gcp.credentials-path`) needs, on that bucket:
- `storage.objects.create` (mint signed PUT URL / write small uploads),
- `storage.objects.get` + `storage.objects.list` (sign read URLs — already needed for reports).

## 3. Bucket CORS (REQUIRED for the browser direct PUT)
The browser uploads straight to GCS via the signed PUT URL, so the bucket must allow PUT/GET from the
app origin. Without this the PUT is blocked by the browser (the client shows
"GCS PUT failed … is the bucket CORS configured for PUT?").

`cors.json`:
```json
[
  {
    "origin": ["http://localhost:8090", "https://<your-app-domain>"],
    "method": ["PUT", "GET", "HEAD"],
    "responseHeader": ["Content-Type"],
    "maxAgeSeconds": 3600
  }
]
```
```bash
gcloud storage buckets update gs://<REPORT_GCS_BUCKET> --cors-file=cors.json
# or: gsutil cors set cors.json gs://<REPORT_GCS_BUCKET>
```

## 4. Cloud Run sizing (sandbox)
DuckDB httpfs scans the file over HTTP range requests, so memory stays bounded, but give the sandbox a
sane floor and enough request time:
```bash
gcloud run services update sandbox-service \
  --memory=2Gi --cpu=2 --timeout=900   # raise memory/timeout for big scans
```
The agent SSE timeout is already 900s (`STREAM_TIMEOUT_MS`). The signed read URL TTL for analysis is 1h.

## 5. Formats
- **CSV / Parquet** → read via DuckDB httpfs (no download, range scans) — the GB-scale path.
- **XLSX** → DuckDB can't read remote xlsx; the sandbox downloads it and uses `pandas.read_excel`
  (fine for ≤ a few hundred MB). **Recommend CSV/Parquet for GB data.**

## How to test
1. In `chat-test.html`, attach a CSV **> 20 MB** (client switches to direct-to-GCS), Deep Analysis ON,
   ask "give me a detailed analysis."
2. Expect logs: `[GCS-SIGN] signed PUT url …` → (browser PUT) → `[GCS-SIGN] (read sign)` →
   `[GCS-ANALYSIS] code attempt …` with `duckdb`/`httpfs` → a data-scientist report + charts, over the
   FULL file (row count > 5,000), flat LLM tokens.
3. "…and give me a PDF" → also emits a Download PDF (built from a DuckDB sample + the narrative).

## True multi-GB streaming (DuckDB httpfs) — OPT-IN, off by default

By default the sandbox **downloads** the file then reads it locally (works to the `DOWNLOAD_MAX_BYTES`
cap; on Cloud Run that download counts against `/tmp` memory). To read **multi-GB files without
downloading**, flip on httpfs streaming — but this **opens a narrow network egress hole** in the
code-execution sandbox, so do it deliberately:

1. **Rebuild the sandbox image** — the Dockerfile now `INSTALL httpfs` at build (pre-bundled into
   `~/.duckdb`), so the runtime needs no DuckDB-extension egress.
2. **Allow egress to GCS ONLY** (allowlist — do NOT open the whole internet). On Cloud Run:
   - attach a **VPC connector** with egress through **Cloud NAT**, and a **firewall/Cloud NAT rule
     allowing only `storage.googleapis.com` (and `199.36.153.8/30` for Private Google Access)**;
   - keep the **metadata server `169.254.169.254` blocked**.
   The sandbox runner now passes TLS/proxy/DNS env through to user code, so once the network allows GCS,
   DuckDB httpfs can reach the signed URL.
3. **Turn on the flag** on the agent service: `SANDBOX_HTTPFS_STREAMING=true`
   (`services.sandbox.httpfs-streaming`). The GCS-analysis + doc paths then read the signed URL directly
   via DuckDB httpfs (no download).
4. **Verify:** large-file analysis logs show `INSTALL httpfs; LOAD httpfs;` + `read_csv_auto('https://…')`
   succeeding with no download; on Cloud Run, instance memory stays flat for a multi-GB file.

> Security note: this lets the sandbox's (model-written) code make outbound calls to **GCS only**. The
> egress restriction is enforced at the **network layer** (VPC/firewall), not in code — verify it.
> Leave `SANDBOX_HTTPFS_STREAMING=false` until that allowlist is in place.

## Not yet done (P3 remainder)
- **pallet-iq (Expo) client** — the large-file upload flow needs porting there too (separate repo; see
  the pallet-iq parity plan).
- **Retire `dataJson` fully** from the small-file doc-render + follow-up storage (currently bounded but
  functional).
