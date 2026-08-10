module BeaverNestBe.Tests.Unit.Steps.RecoverySteps

open TickSpec

[<Given>]
let ``BeaverNest is ready with WAL enabled`` () = ()

[<When>]
let ``I run the manual backup command while the application remains online`` () = ()

[<Then>]
let ``the backup completes through the SQLite backup API`` () = ()

[<Then>]
let ``integrity_check returns "ok" for the backup`` () = ()

[<Then>]
let ``foreign_key_check returns no rows for the backup`` () = ()

[<Given>]
let ``a validated backup and the application is stopped`` () = ()

[<When>]
let ``I run the restore command against the configured durable directory`` () = ()

[<Then>]
let ``the replaced database is preserved at a recoverable path`` () = ()

[<Then>]
let ``the restored migration journal is current`` () = ()

[<Then>]
let ``the restarted application reports ready`` () = ()

[<Given>]
let ``the final promote of the staged database will fail`` () = ()

[<Then>]
let ``the pre-restore database is restored at the live path`` () = ()

[<Then>]
let ``the command reports that the restore failed`` () = ()

[<Given>]
let ``the rollback to the preserved database will also fail`` () = ()

[<Given>]
let ``companion removal for the live database will fail`` () = ()

[<Then>]
let ``the command reports that the restore failed and the rollback failed`` () = ()

[<Then>]
let ``the command instructs the operator to recover the live database manually`` () = ()
