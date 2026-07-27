"""Worked Example 4: The Modern Data Stack's Shape."""  # => co-03: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

PIPELINE_LOG: list[str] = []  # => co-03: records which stage touched the record, IN ORDER, as proof of the shape


def source() -> dict[str, object]:  # => co-03: SOURCE -- where a record originates, outside this pipeline's control
    """Return one raw record, as if read from an upstream application database."""  # => co-03: documents source's contract -- no runtime output, just sets its __doc__
    PIPELINE_LOG.append("source")  # => co-03: log this stage's participation
    return {"order_id": 2001, "amount_text": "88.00", "region": "east"}  # => co-03: a RAW record -- untyped amount


def ingest(record: dict[str, object]) -> dict[str, object]:  # => co-03: INGEST (EL) -- extract + load, no shaping yet
    """Land the record as-is, adding only pipeline metadata -- no shaping of the business fields."""  # => co-03: documents ingest's contract -- no runtime output, just sets its __doc__
    PIPELINE_LOG.append("ingest")  # => co-03: log this stage's participation
    return {**record, "_ingested": True}  # => co-03: EL means Extract+Load -- copy through, tag it, nothing more


def transform(record: dict[str, object]) -> dict[str, object]:  # => co-03: TRANSFORM (T) -- the shaping step
    """Type and shape the record for consumption -- the pipeline's one shaping step."""  # => co-03: documents transform's contract -- no runtime output, just sets its __doc__
    PIPELINE_LOG.append("transform")  # => co-03: log this stage's participation
    return {"order_id": record["order_id"], "amount": float(record["amount_text"]), "region": record["region"]}  # => co-03: typed + shaped


def serve(record: dict[str, object]) -> str:  # => co-03: SERVE -- the record's final, consumption-ready form
    """Render the record as a one-line summary, as if handed to a BI dashboard or an ML feature store."""  # => co-03: documents serve's contract -- no runtime output, just sets its __doc__
    PIPELINE_LOG.append("serve")  # => co-03: log this stage's participation
    return f"order {record['order_id']}: ${record['amount']:.2f} ({record['region']})"  # => co-03: the served, human-readable form


if __name__ == "__main__":  # => co-03: entry point -- runs only when this file executes directly, not on import
    raw_record = source()  # => co-03: stage 1 -- SOURCE
    ingested_record = ingest(raw_record)  # => co-03: stage 2 -- INGEST (EL)
    transformed_record = transform(ingested_record)  # => co-03: stage 3 -- TRANSFORM (T)
    served_summary = serve(transformed_record)  # => co-03: stage 4 -- SERVE
    print(f"Pipeline stages, in order: {PIPELINE_LOG}")  # => co-03: prints the exact stage order the record traveled
    print(f"Served output -> {served_summary!r}")  # => co-03: prints the final, consumption-ready form
    assert PIPELINE_LOG == ["source", "ingest", "transform", "serve"], "all four stages must run in the canonical order"  # => co-03
    assert served_summary == "order 2001: $88.00 (east)", "the record must arrive at serve fully typed and shaped"  # => co-03
    print("MATCH: one record flowed end to end through source -> ingest -> transform -> serve")  # => co-03
    # => co-03: source->ingest(EL)->transform(T)->serve is the canonical shape every later worked example specializes
