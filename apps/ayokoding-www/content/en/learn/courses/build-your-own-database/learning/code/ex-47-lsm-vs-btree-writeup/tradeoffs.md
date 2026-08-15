# LSM versus B-tree

A B-tree updates pages in place and favors predictable point and range reads. An LSM absorbs writes in a memtable then writes sorted immutable runs, trading write locality for compaction work and potentially higher read amplification. See [SQLite's B-tree format](https://www.sqlite.org/fileformat2.html) and [Database Internals](https://www.oreilly.com/library/view/database-internals/9781492040330/).
