module BeaverNestBe.Tests.Unit.Tests.StaticRoutingTests

open System.Net
open Xunit
open BeaverNestBe.WebApp
open BeaverNestBe.Tests.Unit.Steps.BddState

// @covers specs/apps/beavernest/behavior/beavernest-be/gherkin/routing/missing-asset.feature:Unknown static asset is not replaced by the SPA shell
[<Fact>]
let ``missing static asset returns a real 404 instead of the SPA shell`` () =
    let client = buildStaticClient webApp
    let response = client.GetAsync("/assets/missing.js").Result
    let body = response.Content.ReadAsStringAsync().Result
    Assert.Equal(HttpStatusCode.NotFound, response.StatusCode)
    Assert.DoesNotContain("id=\"root\"", body)

// @covers specs/apps/beavernest/behavior/beavernest-app/gherkin/cache-update.feature:Normal navigation receives a fresh hosted Flutter bundle
[<Fact>]
let ``unhashed Flutter entrypoint revalidates on every normal navigation`` () =
    let client = buildStaticClient webApp
    let response = client.GetAsync("/main.dart.js").Result

    Assert.Equal(HttpStatusCode.OK, response.StatusCode)
    Assert.Equal("no-cache", response.Headers.GetValues("Cache-Control") |> Seq.exactlyOne)

// @covers specs/apps/beavernest/behavior/beavernest-be/gherkin/routing/spa-fallback.feature:Unknown client route receives the SPA shell
[<Fact>]
let ``unknown dotless client route returns the Flutter application shell`` () =
    let client = buildStaticClient webApp
    let response = client.GetAsync("/future-client-route").Result
    let body = response.Content.ReadAsStringAsync().Result
    Assert.Equal(HttpStatusCode.OK, response.StatusCode)
    Assert.Contains("flutter_bootstrap.js", body)
    Assert.Equal("no-cache", response.Headers.GetValues("Cache-Control") |> Seq.exactlyOne)

[<Theory>]
[<InlineData("/api/v1/does-not-exist")>]
[<InlineData("/assets/missing.js")>]
[<InlineData("/future-client-route.js")>]
let ``API asset and file-like paths never receive the SPA shell`` (path: string) =
    let client = buildStaticClient webApp
    let response = client.GetAsync(path).Result
    let body = response.Content.ReadAsStringAsync().Result
    Assert.Equal(HttpStatusCode.NotFound, response.StatusCode)
    Assert.DoesNotContain("flutter_bootstrap.js", body)
