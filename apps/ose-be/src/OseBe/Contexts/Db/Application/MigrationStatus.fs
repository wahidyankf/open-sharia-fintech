namespace OseBe.Contexts.Db

/// Application-owned lifecycle state for database migrations.
module Application =

    /// The observable migration state of the current backend process.
    type MigrationState =
        | Pending
        | Applied

    /// Renders the migration state for the public system-status contract.
    let stateToString (state: MigrationState) : string =
        match state with
        | Pending -> "pending"
        | Applied -> "applied"

    /// Thread-safe process-local migration status shared with the HTTP route.
    type SharedMigrationStatus() =
        let mutable state = Pending
        let gate = obj ()

        /// Records that every pending migration completed successfully.
        member _.MarkApplied() = lock gate (fun () -> state <- Applied)

        /// Reads the current process migration state.
        member _.Get() = lock gate (fun () -> state)

    /// Creates a migration status initialized to pending.
    let newMigrationStatus () = SharedMigrationStatus()

    /// Creates the already-applied status used by in-process route tests.
    let appliedMigrationStatus () =
        let status = newMigrationStatus ()
        status.MarkApplied()
        status
