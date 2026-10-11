-- SQL models over raw.snapshot (one row per role per daily tracker.csv).
--
--   stg.snapshot      typed postings only; personal columns dropped
--   int.id_alias      watcher ids that were renamed, stitched by URL
--   int.source_start  the first day each source (board) was watched
--   mart.role_day     the daily table: one row per role per day it was listed
--   mart.role         one row per role: when it opened, when it closed
--   mart.daily_market open / new / closed counts per day and category
--
-- Rebuilt in full by market/backfill.py; every statement is idempotent.

CREATE SCHEMA IF NOT EXISTS stg;
CREATE SCHEMA IF NOT EXISTS int;
CREATE SCHEMA IF NOT EXISTS mart;

-- ── staging ─────────────────────────────────────────────────────────────────
-- Watchlist and planned rows are career hubs and forecasts, not postings.
-- The earliest snapshots predate record_kind, so status decides for them.
-- my_status / priority / applied_date / notes were personal columns in July's
-- files; they are never selected.
CREATE OR REPLACE TABLE stg.snapshot AS
SELECT
    snapshot_date,
    id                                            AS watcher_id,
    nullif(trim(url), '')                         AS url,
    trim(company)                                 AS company,
    trim(role)                                    AS title,
    coalesce(nullif(category, ''), 'Unknown')     AS category,
    coalesce(nullif(region, ''), 'Unknown')       AS region,
    coalesce(nullif(company_type, ''), 'unknown') AS company_type,
    coalesce(nullif(elite_tier, ''), 'none')      AS elite_tier,
    coalesce(nullif(role_type, ''), 'unknown')    AS role_type,
    coalesce(nullif(term, ''), 'Unknown')         AS term,
    coalesce(nullif(level, ''), 'Unknown')        AS level,
    coalesce(nullif(sponsorship, ''), 'unknown')  AS sponsorship,
    coalesce(nullif(citizenship, ''), 'unknown')  AS citizenship,
    coalesce(nullif(work_mode, ''), 'unspecified') AS work_mode,
    coalesce(sources, '')                         AS sources,
    source_status,
    CASE
        WHEN source_status = 'open' THEN 'open'
        WHEN source_status IN ('gone/closed?', 'closed') THEN 'closed'
        ELSE 'stale'      -- stale/not-seen, stale/source-error: not yet known
    END                                           AS status,
    try_cast(nullif(first_seen, '') AS DATE)      AS tracker_first_seen,
    try_cast(nullif(deadline, '') AS DATE)        AS deadline
FROM raw.snapshot
WHERE coalesce(nullif(record_kind, ''), 'posting') = 'posting'
  AND source_status NOT IN ('watchlist', 'planned');

-- ── id stitching ────────────────────────────────────────────────────────────
-- The watcher's id is built from company, title and location, so a retitled
-- advert gets a new id. When an id vanishes and the next day's file lists the
-- same URL under a different id, that is one role, not a closure and a new
-- posting. Chains are followed back to the first id, which becomes role_key.
CREATE OR REPLACE TABLE int.id_alias AS
WITH RECURSIVE days AS (
    SELECT snapshot_date AS d, lead(snapshot_date) OVER (ORDER BY snapshot_date) AS next_d
    FROM (SELECT DISTINCT snapshot_date FROM stg.snapshot)
),
ids AS (SELECT DISTINCT snapshot_date AS d, watcher_id, url FROM stg.snapshot),
last_day AS (SELECT watcher_id, max(d) AS d FROM ids GROUP BY 1),
edges AS (
    -- old id last listed on day d; a new id carries its URL on day d+1 and was
    -- never listed before then.
    SELECT DISTINCT ON (o.watcher_id) o.watcher_id AS old_id, n.watcher_id AS new_id
    FROM last_day l
    JOIN ids o ON o.watcher_id = l.watcher_id AND o.d = l.d
    JOIN days ON days.d = l.d
    JOIN ids n ON n.d = days.next_d AND n.url = o.url AND n.watcher_id <> o.watcher_id
    WHERE o.url IS NOT NULL
      AND NOT EXISTS (SELECT 1 FROM ids p WHERE p.watcher_id = n.watcher_id AND p.d <= l.d)
    ORDER BY o.watcher_id, n.watcher_id
),
chain(watcher_id, role_key) AS (
    SELECT DISTINCT watcher_id, watcher_id FROM ids
    WHERE watcher_id NOT IN (SELECT new_id FROM edges)
    UNION ALL
    SELECT e.new_id, c.role_key FROM chain c JOIN edges e ON e.old_id = c.watcher_id
)
SELECT watcher_id, role_key FROM chain;

-- ── source coverage ─────────────────────────────────────────────────────────
-- A role whose every source started being watched the day it was first seen
-- was not posted that day: the tracker simply started looking. Its age at
-- discovery is unknown, so it is left out of duration analysis.
CREATE OR REPLACE TABLE int.source_start AS
SELECT source, min(snapshot_date) AS first_watched
FROM (
    SELECT snapshot_date, trim(unnest(string_split(sources, ','))) AS source
    FROM stg.snapshot
)
WHERE source <> ''
GROUP BY 1;

-- ── the daily table ─────────────────────────────────────────────────────────
CREATE OR REPLACE TABLE mart.role_day AS
SELECT a.role_key, s.*
FROM stg.snapshot s
JOIN int.id_alias a USING (watcher_id);

-- ── one row per role ────────────────────────────────────────────────────────
CREATE OR REPLACE TABLE mart.role AS
WITH calendar AS (
    SELECT snapshot_date AS d, lead(snapshot_date) OVER (ORDER BY snapshot_date) AS next_d
    FROM (SELECT DISTINCT snapshot_date FROM stg.snapshot)
),
bounds AS (SELECT min(d) AS first_day, max(d) AS last_day FROM calendar),
per_role AS (
    SELECT
        role_key,
        -- attributes as the tracker last described them
        arg_max(company, snapshot_date)      AS company,
        arg_max(title, snapshot_date)        AS title,
        arg_max(category, snapshot_date)     AS category,
        arg_max(region, snapshot_date)       AS region,
        arg_max(company_type, snapshot_date) AS company_type,
        arg_max(elite_tier, snapshot_date)   AS elite_tier,
        arg_max(role_type, snapshot_date)    AS role_type,
        arg_max(term, snapshot_date)         AS term,
        arg_max(level, snapshot_date)        AS level,
        arg_max(sponsorship, snapshot_date)  AS sponsorship,
        arg_max(work_mode, snapshot_date)    AS work_mode,
        arg_max(url, snapshot_date)          AS url,
        arg_max(deadline, snapshot_date)     AS deadline,
        string_agg(DISTINCT sources, ',')    AS all_sources,
        min(snapshot_date)                   AS first_listed,
        min(snapshot_date) FILTER (WHERE status = 'open') AS opened_on,
        max(snapshot_date) FILTER (WHERE status = 'open') AS last_open,
        max(snapshot_date)                   AS last_listed,
        arg_max(status, snapshot_date)       AS final_status,
        count(*) FILTER (WHERE status = 'open') AS days_listed_open,
        count(DISTINCT watcher_id)           AS watcher_ids
    FROM mart.role_day
    GROUP BY role_key
),
sourced AS (
    SELECT p.role_key, min(ss.first_watched) AS earliest_source_start
    FROM per_role p,
         unnest(string_split(p.all_sources, ',')) AS t(source)
    JOIN int.source_start ss ON ss.source = trim(t.source)
    GROUP BY 1
)
SELECT
    p.*,
    -- closed: the tracker confirmed it gone (two healthy misses) and it never
    -- came back. The closure is dated to the first day it was missing.
    (p.final_status = 'closed' AND p.last_open IS NOT NULL)          AS closed,
    CASE WHEN p.final_status = 'closed' THEN c.next_d END            AS closed_on,
    -- duration in days from first open listing to closure, or to the last
    -- day it was seen open when still open / dropped / unconfirmed (censored)
    CASE WHEN p.final_status = 'closed' THEN datediff('day', p.opened_on, c.next_d)
         ELSE datediff('day', p.opened_on, p.last_open) + 1 END      AS duration_days,
    -- fresh: some source that lists it was already being watched before the
    -- role appeared, and the scraper code did not change that day, so
    -- opened_on is (within a day) when it was posted.
    (s.earliest_source_start < p.opened_on AND p.opened_on > b.first_day
     AND p.opened_on NOT IN (SELECT snapshot_date FROM raw.coverage_change)) AS fresh,
    (p.days_listed_open < datediff('day', p.opened_on, p.last_open) + 1) AS reopened,
    CASE
        WHEN p.all_sources LIKE '%Simplify%' OR p.all_sources LIKE '%vanshb03%'
          OR p.all_sources LIKE '%sndsh404%'                 THEN 'community list'
        WHEN p.all_sources LIKE '%Greenhouse/%'
          OR p.all_sources LIKE '%Ashby/%'
          OR p.all_sources LIKE '%Lever/%'                   THEN 'company ATS'
        ELSE 'other'
    END                                                              AS source_family,
    count(*) OVER (PARTITION BY p.company)                           AS company_roles
FROM per_role p
JOIN calendar c ON c.d = p.last_open
LEFT JOIN sourced s USING (role_key)
CROSS JOIN bounds b
WHERE p.opened_on IS NOT NULL;

-- ── the market, day by day ──────────────────────────────────────────────────
CREATE OR REPLACE TABLE mart.daily_market AS
SELECT
    d.snapshot_date,
    r.category,
    count(*) FILTER (WHERE d.status = 'open')                        AS open_roles,
    count(*) FILTER (WHERE r.opened_on = d.snapshot_date AND r.fresh) AS new_roles,
    count(*) FILTER (WHERE r.closed_on = d.snapshot_date)            AS closed_roles
FROM mart.role_day d
JOIN mart.role r USING (role_key)
GROUP BY ALL;
