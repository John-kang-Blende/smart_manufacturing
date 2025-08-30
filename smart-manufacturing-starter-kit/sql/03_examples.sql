-- Example queries
-- 1) Overdue jobs
SELECT job_id, tat_seconds, due_ts
FROM v_job_tat
WHERE (now() - due_ts) > interval '0 seconds';

-- 2) Top busy machines (proxy bottlenecks)
SELECT machine_code, run_seconds
FROM v_oee_lite
ORDER BY run_seconds DESC
LIMIT 10;

-- 3) Simple anomaly flag using z-score on reading s1
WITH z AS (
  SELECT ts, machine_id, s1,
         (s1 - AVG(s1) OVER w) / NULLIF(stddev_pop(s1) OVER w, 0) AS z1
  FROM readings
  WINDOW w AS (PARTITION BY machine_id ORDER BY ts ROWS BETWEEN 200 PRECEDING AND CURRENT ROW)
)
SELECT * FROM z WHERE ABS(z1) > 3;
