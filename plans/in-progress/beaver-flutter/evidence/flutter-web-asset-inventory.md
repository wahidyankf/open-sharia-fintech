# Flutter Web Asset Inventory

**Recorded**: 2026-08-13

The production `fvm flutter build web` inventory was built twice. The deliberately rendered
`buildVersion` changed from `v1` to `v2`; the raw observed SHA-256 diff is in
[flutter-web-v1-v2.diff](./flutter-web-v1-v2.diff). It changes the un-hashed
`flutter_bootstrap.js` and `main.dart.js` paths, so neither is immutable.

| Served path class            | Observed files                                                                    | Cache-Control policy                                           |
| ---------------------------- | --------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| HTML entry/fallback          | `index.html`                                                                      | `no-cache`                                                     |
| Bootstrap and loader scripts | `flutter.js`, `flutter_bootstrap.js`, `main.dart.js`, `flutter_service_worker.js` | `no-cache`                                                     |
| Manifest and version data    | `manifest.json`, `version.json`                                                   | `no-cache`                                                     |
| CanvasKit                    | `canvaskit/**`                                                                    | `no-cache`                                                     |
| Fonts and framework assets   | `assets/**`, `icons/**`, `favicon.png`                                            | `no-cache`                                                     |
| Content-addressed file names | No such file name was observed in this Flutter 3.41.5 output                      | Immutable only after a future inventory proves a filename hash |

Every production asset path observed in this inventory is un-hashed. Normal navigation therefore
revalidates the complete hosted bundle, and the custom Flutter bootstrap intentionally does not
register a service worker.
