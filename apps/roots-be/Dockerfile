# Production multi-stage Dockerfile for roots-be (Go / Gin).
# Build context: repo root (e.g. `docker build -f apps/roots-be/Dockerfile .`).
#
# NOTE: the build needs the generated OpenAPI types under
# apps/roots-be/generated-contracts/ (gitignored except for config.yaml). Run
# `nx run roots-be:codegen` before building so they are present in the context.

# Stage 1: compile a static binary.
FROM golang:1.26 AS build
WORKDIR /src

# Copy the module files first so the dependency layer caches independently of
# source edits.
COPY apps/roots-be/go.mod apps/roots-be/go.sum ./
RUN go mod download

COPY apps/roots-be/ ./

# CGO_ENABLED=0 makes the binary static so the runtime stage can be scratch.
# -trimpath keeps build-machine paths out of the binary, which also stops a
# local absolute path from being baked into a published image.
RUN CGO_ENABLED=0 GOOS=linux go build -trimpath -ldflags="-s -w" \
  -o /out/roots-be ./cmd/roots-be

# Stage 2: scratch runtime. The binary is static, so the image needs nothing
# else -- no shell, no package manager, nothing to pivot through.
#
# distroless would be the conventional choice here, but it lives on gcr.io,
# which .hadolint.yaml does not list under trustedRegistries. scratch reaches
# the same minimal-surface result without widening that allowlist, which would
# be a repo-rules change well outside this delivery unit.
#
# No CA certificates are copied in: roots-be makes no outbound TLS calls. Add
# them here the moment it does, or every HTTPS request will fail x509 verification.
FROM scratch AS runtime

COPY --from=build /out/roots-be /roots-be

# Matches config.DefaultPort. EXPOSE is documentation, not a binding.
EXPOSE 8402

# Numeric UID rather than a name: scratch has no /etc/passwd to resolve one
# against, and the kernel only needs the number. 65532 is the conventional
# non-root UID used by distroless.
USER 65532:65532

ENTRYPOINT ["/roots-be"]
