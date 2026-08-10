module BeaverNestBe.Tests.Unit.Tests.SecurityHeaderTests

open System.Net.Http
open Xunit
open BeaverNestBe.WebApp
open BeaverNestBe.Tests.Unit.Steps.BddState

let private expectedHeaders =
    [ "Content-Security-Policy",
      "default-src 'self'; base-uri 'self'; object-src 'none'; frame-ancestors 'none'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'self'"
      "X-Content-Type-Options", "nosniff"
      "Referrer-Policy", "strict-origin-when-cross-origin"
      "X-Frame-Options", "DENY"
      "Permissions-Policy", "camera=(), microphone=(), geolocation=()" ]

let private assertSecurityHeaders (response: HttpResponseMessage) =
    for name, expectedValue in expectedHeaders do
        let actualValue = response.Headers.GetValues(name) |> Seq.exactlyOne
        Assert.Equal(expectedValue, actualValue)

    Assert.False(response.Headers.Contains("Server"))

[<Theory>]
[<InlineData("/api/v1/health")>]
[<InlineData("/api/v1/does-not-exist")>]
[<InlineData("/assets/app-12345678.js")>]
[<InlineData("/index.html")>]
[<InlineData("/future-client-route")>]
let ``every API static and SPA response carries the global security policy`` (path: string) =
    let client = buildStaticClient webApp
    let response = client.GetAsync(path).Result
    assertSecurityHeaders response
