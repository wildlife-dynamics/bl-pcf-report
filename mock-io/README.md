# Mock-IO data

Synthetic example returns for the IO tasks, used by the `mock_io` test cases in
`test-cases.yaml` (see `.github/workflows/test.yml`, which points the
`WT_TASK_MOCK_IO__…` environment variables at these files).

They have the same columns and types as the real EarthRanger livestock predation events
(`hwc_lvstprd`), and the choice fields use the same option values, but every name, ID,
note, date, number and location is made up. Locations are random points inside the
public Amboseli group-ranch polygons shipped with ext-big-life.

| File | Mocks |
|---|---|
| `get-events.example-return.parquet` | `ecoscope.platform.tasks.io.get_events` |
| `process-events-details.example-return.parquet` | `ecoscope.platform.tasks.io.process_events_details` |
