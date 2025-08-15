

CREATE TABLE [dbo].[DialpadCalls] (
    call_id VARCHAR(50) PRIMARY KEY,
    contact_email VARCHAR(255),
    contact_id VARCHAR(50),
    contact_name VARCHAR(255),
    contact_phone VARCHAR(50),
    contact_type VARCHAR(50),
    date_connected DATETIME2,
    date_ended DATETIME2,
    date_started DATETIME2,
    direction VARCHAR(50),
    duration DECIMAL(18, 6),
    entry_point_target_id VARCHAR(50),
    event_timestamp DATETIME2,
    external_number VARCHAR(50),
    internal_number VARCHAR(50),
    is_transferred BIT,
    mos_score DECIMAL(3, 2),
    proxy_target_id VARCHAR(50),
    state VARCHAR(50),
    target_email VARCHAR(255),
    target_id VARCHAR(50),
    target_name VARCHAR(255),
    target_phone VARCHAR(50),
    target_type VARCHAR(50),
    total_duration DECIMAL(18, 6),
    was_recorded BIT
);
CREATE INDEX IX_DialpadCalls_ContactEmail ON dbo.DialpadCalls (contact_email);

ALTER TABLE [dbo].[DialpadCalls]
ADD transcript NVARCHAR(MAX);