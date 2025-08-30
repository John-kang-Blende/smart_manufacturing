-- Manufacturing schema (PostgreSQL/Timescale-friendly)
CREATE TABLE IF NOT EXISTS machines (
  id SERIAL PRIMARY KEY,
  machine_code TEXT UNIQUE,
  line TEXT
);

CREATE TABLE IF NOT EXISTS sensors (
  id SERIAL PRIMARY KEY,
  machine_id INT REFERENCES machines(id),
  name TEXT
);

CREATE TABLE IF NOT EXISTS readings (
  ts TIMESTAMP NOT NULL,
  machine_id INT REFERENCES machines(id),
  s1 DOUBLE PRECISION,
  s2 DOUBLE PRECISION,
  s3 DOUBLE PRECISION,
  s4 DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS jobs (
  id SERIAL PRIMARY KEY,
  route INT,
  due_ts TIMESTAMP,
  arrive_ts TIMESTAMP
);

CREATE TABLE IF NOT EXISTS operations (
  id SERIAL PRIMARY KEY,
  job_id INT REFERENCES jobs(id),
  machine_id INT REFERENCES machines(id),
  start_ts TIMESTAMP,
  end_ts TIMESTAMP
);

CREATE TABLE IF NOT EXISTS spc_limits (
  id SERIAL PRIMARY KEY,
  line TEXT,
  metric TEXT,
  mu DOUBLE PRECISION,
  sigma DOUBLE PRECISION,
  created_at TIMESTAMP DEFAULT now()
);
