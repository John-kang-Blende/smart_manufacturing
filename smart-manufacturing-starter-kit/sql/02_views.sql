-- Analytic views
CREATE OR REPLACE VIEW v_job_tat AS
SELECT j.id AS job_id,
       EXTRACT(EPOCH FROM (MAX(o.end_ts) - MIN(j.arrive_ts))) AS tat_seconds,
       j.due_ts
FROM jobs j
JOIN operations o ON o.job_id = j.id
GROUP BY j.id, j.due_ts;

CREATE OR REPLACE VIEW v_oee_lite AS
SELECT m.machine_code,
       SUM(EXTRACT(EPOCH FROM (o.end_ts - o.start_ts))) AS run_seconds,
       COUNT(*) AS ops_count
FROM machines m
LEFT JOIN operations o ON o.machine_id = m.id
GROUP BY m.machine_code;
