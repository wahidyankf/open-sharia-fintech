# Phase 5 Container Base-Image Adoption Evidence

## Decision Record

- Selection date: 2026-08-03
- Path B cutoff: 2026-08-03 − 60 days = 2026-06-04.
- Path A applies to .NET 10 because it is the current Microsoft LTS line, supported through November 2028. Path A selects its latest servicing/runtime patch and corresponding SDK feature band.
- Rule 5a: .NET 10.0.10 is the latest LTS runtime/ASP.NET servicing release; SDK 10.0.302 is the
  matching latest SDK feature band published for that servicing release.
- Rule 5b: MCR tag inspection confirms each selected image resolves to the recorded immutable manifest;
  neither Microsoft release notes nor the image-maintainer release record contains a release-blocker
  for this F# build or ASP.NET runtime use.

| Image                             | Exact tag and immutable digest                                                               | Path | Release date | Clearance | `FROM` occurrences                                                                                                                                 |
| --------------------------------- | -------------------------------------------------------------------------------------------- | ---- | ------------ | --------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `docker.io/library/node`          | `24.16.0-alpine3.23@sha256:2bdb65ed1dab192432bc31c95f94155ca5ad7fc1392fb7eb7526ab682fa5bf14` | A    | 2026-05-21   | **CLEAR** | `apps/beaver-nest-be/Dockerfile` build; `infra/dev/beaver-nest-app/Dockerfile.fe.dev`; retained `apps/beaver-nest-fe/Dockerfile` build and runtime |
| `mcr.microsoft.com/dotnet/sdk`    | `10.0.302-noble@sha256:72dd743782f2ae7e5476fd64f6a460045e3998dc862218b80e6944cba79a01b0`     | A    | 2026-07-14   | **CLEAR** | `apps/beaver-nest-be/Dockerfile` build; `apps/beaver-nest-be/Dockerfile.integration`; `infra/dev/beaver-nest-app/Dockerfile.be.dev`                |
| `mcr.microsoft.com/dotnet/aspnet` | `10.0.10-noble@sha256:f1126d438ccc359f51cc6d4701a8deae513856cf10f5fe645d29ea6403dcac6b`      | A    | 2026-07-14   | **CLEAR** | `apps/beaver-nest-be/Dockerfile` runtime                                                                                                           |

## Security Clearance

NVD, GitHub Advisories, Snyk, Microsoft/.NET vendor release and security pages, and the CISA KEV
catalog were checked on the selection date for the selected .NET 10 servicing line and Node LTS base.
No unpatched, applicable image-level CVE was identified. No CVSS 7.0-or-higher selected-image CVE
required an EPSS lookup; no KEV match exists. .NET 10.0.10 is explicitly identified by Microsoft as a
security patch, so the exact SDK/runtime pair is selected under Path A rather than retaining a stale
floating `10.0` tag.

## Sources and Reproducibility

- [Microsoft .NET 10 download record](https://dotnet.microsoft.com/en-us/download/dotnet/10.0)
- [Microsoft .NET release and support policy](https://learn.microsoft.com/en-us/dotnet/core/releases-and-support)
- [MCR .NET 10 default-image compatibility note](https://learn.microsoft.com/en-us/dotnet/core/compatibility/containers/10.0/default-images-use-ubuntu)
- [NVD](https://nvd.nist.gov/)
- [GitHub Advisory Database](https://github.com/advisories)
- [Snyk container database](https://security.snyk.io/)
- [CISA KEV catalog](https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json)

```bash
docker buildx imagetools inspect mcr.microsoft.com/dotnet/sdk:10.0.302-noble --format '{{.Manifest.Digest}}'
docker buildx imagetools inspect mcr.microsoft.com/dotnet/aspnet:10.0.10-noble --format '{{.Manifest.Digest}}'
docker buildx imagetools inspect docker.io/library/node:24.16.0-alpine3.23 --format '{{.Manifest.Digest}}'
```
