module BeaverNestBe.Api.StaticContent

open System
open System.IO
open Microsoft.AspNetCore.Builder
open Microsoft.AspNetCore.Hosting
open Microsoft.AspNetCore.Http
open Microsoft.AspNetCore.StaticFiles
open Microsoft.Extensions.DependencyInjection
open Microsoft.Net.Http.Headers
open Giraffe

let private isApiPath (path: string) =
    path = "/api" || path.StartsWith("/api/", StringComparison.Ordinal)

let private isAssetPath (path: string) =
    path = "/assets" || path.StartsWith("/assets/", StringComparison.Ordinal)

let private isDotlessFinalSegment (path: string) =
    let finalSegment = path.TrimEnd('/').Split('/') |> Array.last
    not (finalSegment.Contains('.'))

let staticFileOptions =
    let options = StaticFileOptions()

    options.OnPrepareResponse <-
        fun context ->
            // The Flutter 3.41.5 release inventory contains only un-hashed
            // asset names. Revalidate every static response until a future
            // inventory proves a content-addressed filename safe to retain.
            context.Context.Response.Headers[HeaderNames.CacheControl] <- "no-cache"

    options

let spaFallbackHandler: HttpHandler =
    fun next context ->
        let path = context.Request.Path.Value

        let isGetOrHead =
            context.Request.Method = HttpMethods.Get
            || context.Request.Method = HttpMethods.Head

        if
            isGetOrHead
            && not (isApiPath path)
            && not (isAssetPath path)
            && isDotlessFinalSegment path
        then
            let environment = context.RequestServices.GetRequiredService<IWebHostEnvironment>()
            let indexPath = Path.Combine(environment.WebRootPath, "index.html")

            if File.Exists(indexPath) then
                context.Response.Headers[HeaderNames.CacheControl] <- "no-cache"
                htmlFile indexPath next context
            else
                skipPipeline
        else
            skipPipeline
