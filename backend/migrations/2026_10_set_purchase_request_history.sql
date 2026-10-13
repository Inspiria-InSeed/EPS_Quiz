-- Preserve every set purchase request and its admin decision.
-- Existing databases created before request history was enabled have a
-- per-student/per-set uniqueness constraint; remove it so a rejected or
-- completed request can be submitted again without overwriting history.
ALTER TABLE student_set_purchase_requests
    DROP CONSTRAINT IF EXISTS uq_student_set_purchase_request;

CREATE INDEX IF NOT EXISTS ix_student_set_purchase_requests_student_set_date
    ON student_set_purchase_requests (student_id, exam_set_id, requested_at DESC);
