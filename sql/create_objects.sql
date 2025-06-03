-- Initial Table Definitions (as originally provided)

-- Table: dbo.LoanPASS_Product_Offerings
-- Represents the main Product Offering object.
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[LoanPASS_Product_Offerings]') AND type in (N'U'))
BEGIN
    PRINT 'Creating dbo.LoanPASS_Product_Offerings...';
    CREATE TABLE dbo.LoanPASS_Product_Offerings (
        -- Internal SQL Primary Key
        Id INT IDENTITY(1,1) PRIMARY KEY,

        -- System Fields
        Name NVARCHAR(255) NULL,
        CreatedDate DATETIMEOFFSET NULL,
        LastModifiedDate DATETIMEOFFSET NULL,
        IsDeleted BIT DEFAULT 0 NOT NULL,

        -- Custom Fields
        Product_Id__c NVARCHAR(255) NULL UNIQUE,
        Product_Name__c NVARCHAR(255) NULL,
        Product_Code__c NVARCHAR(255) NULL,
        Investor_Name__c NVARCHAR(255) NULL,
        Investor_Code__c NVARCHAR(255) NULL,
        Is_Pricing_Enabled__c BIT NULL,
        Status__c NVARCHAR(255) NULL,
        Rate_Sheet_Effective_Timestamp__c DATETIMEOFFSET NULL
    );
END
ELSE
BEGIN
    PRINT 'Table dbo.LoanPASS_Product_Offerings already exists.';
END
GO

---

-- Table: dbo.LoanPASS_Product_Calculated_Fields
-- Stores calculated fields associated with a Product Offering.
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[LoanPASS_Product_Calculated_Fields]') AND type in (N'U'))
BEGIN
    PRINT 'Creating dbo.LoanPASS_Product_Calculated_Fields...';
    CREATE TABLE dbo.LoanPASS_Product_Calculated_Fields (
        -- Internal SQL Primary Key
        Id INT IDENTITY(1,1) PRIMARY KEY,

        -- System Fields
        Name NVARCHAR(255) NULL,
        CreatedDate DATETIMEOFFSET NULL,
        LastModifiedDate DATETIMEOFFSET NULL,
        IsDeleted BIT DEFAULT 0 NOT NULL,

        -- Foreign Key to dbo.LoanPASS_Product_Offerings (using its internal SQL Id)
        LoanPASS_Product_Offering_Id INT NOT NULL,

        -- Custom Fields
        Field_Id__c NVARCHAR(255) NULL,
        Value_Type__c NVARCHAR(255) NULL,
        Enum_Type_Id__c NVARCHAR(255) NULL,
        Variant_Id__c NVARCHAR(255) NULL,
        Number_Value__c DECIMAL(18,2) NULL, -- Will be altered
        String_Value__c NVARCHAR(255) NULL, -- Will be altered
        Duration_Count__c DECIMAL(18,0) NULL,
        Duration_Unit__c NVARCHAR(255) NULL,

        -- Foreign Key Constraint
        CONSTRAINT FK_ProductCalculatedFields_ProductOfferings
            FOREIGN KEY (LoanPASS_Product_Offering_Id)
            REFERENCES dbo.LoanPASS_Product_Offerings(Id)
    );
END
ELSE
BEGIN
    PRINT 'Table dbo.LoanPASS_Product_Calculated_Fields already exists.';
END
GO

---

-- Table: dbo.LoanPASS_Price_Scenarios
-- Represents a specific pricing scenario for a Product Offering.
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[LoanPASS_Price_Scenarios]') AND type in (N'U'))
BEGIN
    PRINT 'Creating dbo.LoanPASS_Price_Scenarios...';
    CREATE TABLE dbo.LoanPASS_Price_Scenarios (
        -- Internal SQL Primary Key
        Id INT IDENTITY(1,1) PRIMARY KEY,

        -- System Fields
        Name NVARCHAR(255) NULL,
        CreatedDate DATETIMEOFFSET NULL,
        LastModifiedDate DATETIMEOFFSET NULL,
        IsDeleted BIT DEFAULT 0 NOT NULL,

        -- Foreign Key to dbo.LoanPASS_Product_Offerings (using its internal SQL Id)
        LoanPASS_Product_Offering_Id INT NOT NULL,

        -- Custom Fields
        Adjusted_Rate__c DECIMAL(18,3) NULL,
        Adjusted_Price__c DECIMAL(18,2) NULL,
        Adjusted_Rate_Lock_Count__c DECIMAL(18,0) NULL,
        Adjusted_Rate_Lock_Unit__c NVARCHAR(255) NULL,
        Undiscounted_Rate__c DECIMAL(18,3) NULL,
        Starting_Adjusted_Rate__c DECIMAL(18,3) NULL,
        Starting_Adjusted_Price__c DECIMAL(18,2) NULL,
        Status__c NVARCHAR(255) NULL,
        -- Scenario_Business_Id__c will be added via ALTER

        -- Foreign Key Constraint
        CONSTRAINT FK_PriceScenarios_ProductOfferings
            FOREIGN KEY (LoanPASS_Product_Offering_Id)
            REFERENCES dbo.LoanPASS_Product_Offerings(Id)
    );
END
ELSE
BEGIN
    PRINT 'Table dbo.LoanPASS_Price_Scenarios already exists.';
END
GO

---

-- Table: dbo.LoanPASS_Price_Scenario_Calculated_Fields
-- Stores calculated fields specific to a Price Scenario.
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[LoanPASS_Price_Scenario_Calculated_Fields]') AND type in (N'U'))
BEGIN
    PRINT 'Creating dbo.LoanPASS_Price_Scenario_Calculated_Fields...';
    CREATE TABLE dbo.LoanPASS_Price_Scenario_Calculated_Fields (
        -- Internal SQL Primary Key
        Id INT IDENTITY(1,1) PRIMARY KEY,

        -- System Fields
        Name NVARCHAR(255) NULL,
        CreatedDate DATETIMEOFFSET NULL,
        LastModifiedDate DATETIMEOFFSET NULL,
        IsDeleted BIT DEFAULT 0 NOT NULL,

        -- Foreign Key to dbo.LoanPASS_Price_Scenarios (using its internal SQL Id)
        LoanPASS_Price_Scenario_Id INT NOT NULL,

        -- Custom Fields
        Field_Id__c NVARCHAR(255) NULL,
        Value_Type__c NVARCHAR(255) NULL,
        Enum_Type_Id__c NVARCHAR(255) NULL,
        Variant_Id__c NVARCHAR(255) NULL,
        Number_Value__c DECIMAL(18,2) NULL, -- Will be altered
        String_Value__c NVARCHAR(255) NULL, -- Will be altered
        Duration_Count__c DECIMAL(18,0) NULL,
        Duration_Unit__c NVARCHAR(255) NULL,

        -- Foreign Key Constraint
        CONSTRAINT FK_PSCalculatedFields_PriceScenarios
            FOREIGN KEY (LoanPASS_Price_Scenario_Id)
            REFERENCES dbo.LoanPASS_Price_Scenarios(Id)
    );
END
ELSE
BEGIN
    PRINT 'Table dbo.LoanPASS_Price_Scenario_Calculated_Fields already exists.';
END
GO

---

-- Table: dbo.LoanPASS_Price_Scenario_Errors
-- Stores error details for a Price Scenario.
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[LoanPASS_Price_Scenario_Errors]') AND type in (N'U'))
BEGIN
    PRINT 'Creating dbo.LoanPASS_Price_Scenario_Errors...';
    CREATE TABLE dbo.LoanPASS_Price_Scenario_Errors (
        -- Internal SQL Primary Key
        Id INT IDENTITY(1,1) PRIMARY KEY,

        -- System Fields
        Name NVARCHAR(255) NULL,
        CreatedDate DATETIMEOFFSET NULL,
        LastModifiedDate DATETIMEOFFSET NULL,
        IsDeleted BIT DEFAULT 0 NOT NULL,

        -- Foreign Key to dbo.LoanPASS_Price_Scenarios (using its internal SQL Id)
        LoanPASS_Price_Scenario_Id INT NOT NULL,

        -- Custom Fields
        Source_Type__c NVARCHAR(255) NULL,      -- Maps to errors[].source.type
        Source_Rule_Id__c NVARCHAR(255) NULL,   -- Maps to errors[].source.ruleId
        Error_Type__c NVARCHAR(255) NULL,       -- Maps to errors[].kind.type
        Error_Field_Id__c NVARCHAR(255) NULL,   -- Maps to errors[].kind.fieldId
        Message__c NVARCHAR(MAX) NULL,          -- To store detailed error messages

        -- Foreign Key Constraint
        CONSTRAINT FK_PSErrors_PriceScenarios
            FOREIGN KEY (LoanPASS_Price_Scenario_Id)
            REFERENCES dbo.LoanPASS_Price_Scenarios(Id)
    );
END
ELSE
BEGIN
    PRINT 'Table dbo.LoanPASS_Price_Scenario_Errors already exists.';
END
GO

--------------------------------------------------------------------------------
-- ALTER STATEMENTS FOR EXISTING TABLES
-- These will run if the tables were just created or already existed.
--------------------------------------------------------------------------------

-- Modify dbo.LoanPASS_Product_Calculated_Fields
PRINT 'Altering dbo.LoanPASS_Product_Calculated_Fields if it exists...';
IF OBJECT_ID(N'[dbo].[LoanPASS_Product_Calculated_Fields]', N'U') IS NOT NULL
BEGIN
    -- Check if Number_Value__c needs alteration
    IF EXISTS (SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('dbo.LoanPASS_Product_Calculated_Fields') AND name = 'Number_Value__c' AND (precision != 28 OR scale != 10))
    BEGIN
        ALTER TABLE dbo.LoanPASS_Product_Calculated_Fields
        ALTER COLUMN Number_Value__c DECIMAL(28,10) NULL;
        PRINT 'Column Number_Value__c in dbo.LoanPASS_Product_Calculated_Fields altered to DECIMAL(28,10).';
    END

    -- Check if String_Value__c needs alteration
    IF EXISTS (SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('dbo.LoanPASS_Product_Calculated_Fields') AND name = 'String_Value__c' AND max_length != -1) -- -1 indicates MAX for NVARCHAR
    BEGIN
        ALTER TABLE dbo.LoanPASS_Product_Calculated_Fields
        ALTER COLUMN String_Value__c NVARCHAR(MAX) NULL;
        PRINT 'Column String_Value__c in dbo.LoanPASS_Product_Calculated_Fields altered to NVARCHAR(MAX).';
    END
    PRINT 'dbo.LoanPASS_Product_Calculated_Fields alteration checks complete.';
END
ELSE
BEGIN
    PRINT 'dbo.LoanPASS_Product_Calculated_Fields does not exist, skipping alteration.';
END
GO

---

-- Modify dbo.LoanPASS_Price_Scenarios
PRINT 'Altering dbo.LoanPASS_Price_Scenarios if it exists...';
IF OBJECT_ID(N'[dbo].[LoanPASS_Price_Scenarios]', N'U') IS NOT NULL
BEGIN
    -- Add Scenario_Business_Id__c column if it doesn't exist
    IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('dbo.LoanPASS_Price_Scenarios') AND name = 'Scenario_Business_Id__c')
    BEGIN
        ALTER TABLE dbo.LoanPASS_Price_Scenarios
        ADD Scenario_Business_Id__c NVARCHAR(255) NULL;
        PRINT 'Column Scenario_Business_Id__c added to dbo.LoanPASS_Price_Scenarios.';
    END
    ELSE
    BEGIN
        PRINT 'Column Scenario_Business_Id__c already exists in dbo.LoanPASS_Price_Scenarios.';
    END

    -- Drop the old unique constraint if it exists (by name)
    IF EXISTS (SELECT * FROM sys.key_constraints WHERE type = 'UQ' AND parent_object_id = OBJECT_ID('dbo.LoanPASS_Price_Scenarios') AND name = 'UQ_Scenario_Business_Id')
    BEGIN
        ALTER TABLE dbo.LoanPASS_Price_Scenarios
        DROP CONSTRAINT UQ_Scenario_Business_Id;
        PRINT 'Old constraint UQ_Scenario_Business_Id dropped from dbo.LoanPASS_Price_Scenarios.';
    END
    
    -- Drop the old unique index if it exists (by name, in case it was created as an index directly)
    IF EXISTS (SELECT * FROM sys.indexes WHERE object_id = OBJECT_ID('dbo.LoanPASS_Price_Scenarios') AND name = 'UQ_Scenario_Business_Id' AND is_unique_constraint = 0 AND is_primary_key = 0)
    BEGIN
        DROP INDEX UQ_Scenario_Business_Id ON dbo.LoanPASS_Price_Scenarios;
        PRINT 'Old index UQ_Scenario_Business_Id dropped from dbo.LoanPASS_Price_Scenarios.';
    END
    PRINT 'dbo.LoanPASS_Price_Scenarios alteration checks complete.';
END
ELSE
BEGIN
    PRINT 'dbo.LoanPASS_Price_Scenarios does not exist, skipping alteration.';
END
GO

---

-- Modify dbo.LoanPASS_Price_Scenario_Calculated_Fields
PRINT 'Altering dbo.LoanPASS_Price_Scenario_Calculated_Fields if it exists...';
IF OBJECT_ID(N'[dbo].[LoanPASS_Price_Scenario_Calculated_Fields]', N'U') IS NOT NULL
BEGIN
    -- Check if Number_Value__c needs alteration
    IF EXISTS (SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('dbo.LoanPASS_Price_Scenario_Calculated_Fields') AND name = 'Number_Value__c' AND (precision != 28 OR scale != 10))
    BEGIN
        ALTER TABLE dbo.LoanPASS_Price_Scenario_Calculated_Fields
        ALTER COLUMN Number_Value__c DECIMAL(28,10) NULL;
        PRINT 'Column Number_Value__c in dbo.LoanPASS_Price_Scenario_Calculated_Fields altered to DECIMAL(28,10).';
    END

    -- Check if String_Value__c needs alteration
    IF EXISTS (SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('dbo.LoanPASS_Price_Scenario_Calculated_Fields') AND name = 'String_Value__c' AND max_length != -1) -- -1 indicates MAX for NVARCHAR
    BEGIN
        ALTER TABLE dbo.LoanPASS_Price_Scenario_Calculated_Fields
        ALTER COLUMN String_Value__c NVARCHAR(MAX) NULL;
        PRINT 'Column String_Value__c in dbo.LoanPASS_Price_Scenario_Calculated_Fields altered to NVARCHAR(MAX).';
    END
    PRINT 'dbo.LoanPASS_Price_Scenario_Calculated_Fields alteration checks complete.';
END
ELSE
BEGIN
    PRINT 'dbo.LoanPASS_Price_Scenario_Calculated_Fields does not exist, skipping alteration.';
END
GO

-- Modify dbo.LoanPASS_Price_Scenario_Errors to add Message__c if it wasn't in the original definition and table exists
PRINT 'Altering dbo.LoanPASS_Price_Scenario_Errors if it exists and Message__c column is missing...';
IF OBJECT_ID(N'[dbo].[LoanPASS_Price_Scenario_Errors]', N'U') IS NOT NULL
BEGIN
    IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('dbo.LoanPASS_Price_Scenario_Errors') AND name = 'Message__c')
    BEGIN
        ALTER TABLE dbo.LoanPASS_Price_Scenario_Errors
        ADD Message__c NVARCHAR(MAX) NULL;
        PRINT 'Column Message__c added to dbo.LoanPASS_Price_Scenario_Errors.';
    END
    ELSE
    BEGIN
        PRINT 'Column Message__c already exists in dbo.LoanPASS_Price_Scenario_Errors.';
    END
    PRINT 'dbo.LoanPASS_Price_Scenario_Errors alteration checks complete.';
END
ELSE
BEGIN
    PRINT 'dbo.LoanPASS_Price_Scenario_Errors does not exist, skipping alteration for Message__c column.';
END
GO

--------------------------------------------------------------------------------
-- CREATE STATEMENTS FOR NEW TABLES (with IF NOT EXISTS)
--------------------------------------------------------------------------------

-- Table: dbo.LoanPASS_Price_Scenario_Rejections
-- Stores rejection details for a Price Scenario, mapping to priceScenarios[].status.rejections array.
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[LoanPASS_Price_Scenario_Rejections]') AND type in (N'U'))
BEGIN
    PRINT 'Creating dbo.LoanPASS_Price_Scenario_Rejections...';
    CREATE TABLE dbo.LoanPASS_Price_Scenario_Rejections (
        -- Internal SQL Primary Key
        Id INT IDENTITY(1,1) PRIMARY KEY,

        -- System Fields
        Name NVARCHAR(255) NULL, -- Can store a summary or be null
        CreatedDate DATETIMEOFFSET NULL,
        LastModifiedDate DATETIMEOFFSET NULL,
        IsDeleted BIT DEFAULT 0 NOT NULL,

        -- Foreign Key to dbo.LoanPASS_Price_Scenarios
        LoanPASS_Price_Scenario_Id INT NOT NULL,

        -- Custom Fields from JSON rejections array
        Source_Type__c NVARCHAR(255) NULL,      -- Maps to rejections[].source.type
        Source_Rule_Id__c NVARCHAR(255) NULL,   -- Maps to rejections[].source.ruleId
        Message__c NVARCHAR(MAX) NULL,          -- Maps to rejections[].message

        -- Foreign Key Constraint
        CONSTRAINT FK_PSRejections_PriceScenarios
            FOREIGN KEY (LoanPASS_Price_Scenario_Id)
            REFERENCES dbo.LoanPASS_Price_Scenarios(Id)
            ON DELETE CASCADE -- Optional: delete rejections if the parent scenario is deleted
    );
END
ELSE
BEGIN
    PRINT 'Table dbo.LoanPASS_Price_Scenario_Rejections already exists.';
END
GO

---

-- Table: dbo.LoanPASS_Price_Scenario_Review_Requirements
-- Stores review requirement details for a Price Scenario, mapping to priceScenarios[].status.reviewRequirements array.
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[LoanPASS_Price_Scenario_Review_Requirements]') AND type in (N'U'))
BEGIN
    PRINT 'Creating dbo.LoanPASS_Price_Scenario_Review_Requirements...';
    CREATE TABLE dbo.LoanPASS_Price_Scenario_Review_Requirements (
        -- Internal SQL Primary Key
        Id INT IDENTITY(1,1) PRIMARY KEY,

        -- System Fields
        Name NVARCHAR(255) NULL,
        CreatedDate DATETIMEOFFSET NULL,
        LastModifiedDate DATETIMEOFFSET NULL,
        IsDeleted BIT DEFAULT 0 NOT NULL,

        -- Foreign Key to dbo.LoanPASS_Price_Scenarios
        LoanPASS_Price_Scenario_Id INT NOT NULL,

        -- Custom Fields (structure is basic as JSON array was empty in example)
        Description__c NVARCHAR(MAX) NULL,      -- A textual description of the review requirement
        Requirement_Type__c NVARCHAR(255) NULL, -- Example: 'Documentation', 'Verification'
        Source_Details__c NVARCHAR(MAX) NULL,   -- Example: Could store rule ID or system component

        -- Foreign Key Constraint
        CONSTRAINT FK_PSReviewRequirements_PriceScenarios
            FOREIGN KEY (LoanPASS_Price_Scenario_Id)
            REFERENCES dbo.LoanPASS_Price_Scenarios(Id)
            ON DELETE CASCADE -- Optional
    );
END
ELSE
BEGIN
    PRINT 'Table dbo.LoanPASS_Price_Scenario_Review_Requirements already exists.';
END
GO

---

-- Table: dbo.LoanPASS_Price_Scenario_Adjustments
-- Stores price, margin, or rate adjustments for a Price Scenario.
-- Maps to arrays like priceAdjustments, marginAdjustments, rateAdjustments, etc.
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[LoanPASS_Price_Scenario_Adjustments]') AND type in (N'U'))
BEGIN
    PRINT 'Creating dbo.LoanPASS_Price_Scenario_Adjustments...';
    CREATE TABLE dbo.LoanPASS_Price_Scenario_Adjustments (
        -- Internal SQL Primary Key
        Id INT IDENTITY(1,1) PRIMARY KEY,

        -- System Fields
        Name NVARCHAR(255) NULL,
        CreatedDate DATETIMEOFFSET NULL,
        LastModifiedDate DATETIMEOFFSET NULL,
        IsDeleted BIT DEFAULT 0 NOT NULL,

        -- Foreign Key to dbo.LoanPASS_Price_Scenarios
        LoanPASS_Price_Scenario_Id INT NOT NULL,

        -- Custom Fields
        Adjustment_Category__c NVARCHAR(100) NOT NULL, -- E.g., 'PriceAdjustment', 'MarginAdjustment', 'RateAdjustment', 'FinalPriceAdjustment', 'FinalMarginAdjustment', 'FinalRateAdjustment'
        Description__c NVARCHAR(MAX) NULL,             -- Description of the adjustment (could be a rule name, field name, etc.)
        Adjustment_Value_Numeric__c DECIMAL(28,10) NULL,-- The numeric value of the adjustment
        Adjustment_Value_Text__c NVARCHAR(MAX) NULL,   -- For non-numeric adjustments or additional details
        Source_Rule_Id__c NVARCHAR(255) NULL,          -- If the adjustment comes from a specific rule
        Source_Field_Id__c NVARCHAR(255) NULL,         -- If the adjustment relates to a specific field
        Notes__c NVARCHAR(MAX) NULL,                   -- Any additional notes

        -- Foreign Key Constraint
        CONSTRAINT FK_PSAdjustments_PriceScenarios
            FOREIGN KEY (LoanPASS_Price_Scenario_Id)
            REFERENCES dbo.LoanPASS_Price_Scenarios(Id)
            ON DELETE CASCADE -- Optional
    );
END
ELSE
BEGIN
    PRINT 'Table dbo.LoanPASS_Price_Scenario_Adjustments already exists.';
END
GO

---

-- Table: dbo.LoanPASS_Price_Scenario_Stipulations
-- Stores stipulation details for a Price Scenario, mapping to priceScenarios[].status.stipulations array.
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[LoanPASS_Price_Scenario_Stipulations]') AND type in (N'U'))
BEGIN
    PRINT 'Creating dbo.LoanPASS_Price_Scenario_Stipulations...';
    CREATE TABLE dbo.LoanPASS_Price_Scenario_Stipulations (
        -- Internal SQL Primary Key
        Id INT IDENTITY(1,1) PRIMARY KEY,

        -- System Fields
        Name NVARCHAR(255) NULL,
        CreatedDate DATETIMEOFFSET NULL,
        LastModifiedDate DATETIMEOFFSET NULL,
        IsDeleted BIT DEFAULT 0 NOT NULL,

        -- Foreign Key to dbo.LoanPASS_Price_Scenarios
        LoanPASS_Price_Scenario_Id INT NOT NULL,

        -- Custom Fields (structure is basic as JSON array was empty in example)
        Description__c NVARCHAR(MAX) NOT NULL,    -- A textual description of the stipulation (likely the main content)
        Stipulation_Code__c NVARCHAR(100) NULL, -- An optional code for the stipulation
        Source_Details__c NVARCHAR(MAX) NULL,   -- Example: Could store rule ID or system component that generated it
        Is_Satisfied__c BIT DEFAULT 0 NULL,     -- To track if the stipulation has been met

        -- Foreign Key Constraint
        CONSTRAINT FK_PSStipulations_PriceScenarios
            FOREIGN KEY (LoanPASS_Price_Scenario_Id)
            REFERENCES dbo.LoanPASS_Price_Scenarios(Id)
            ON DELETE CASCADE -- Optional
    );
END
ELSE
BEGIN
    PRINT 'Table dbo.LoanPASS_Price_Scenario_Stipulations already exists.';
END
GO

-- Add Run_Id to dbo.LoanPASS_Product_Offerings
ALTER TABLE dbo.LoanPASS_Product_Offerings
ADD Run_Id VARCHAR(50);

-- Add Run_Id to dbo.LoanPASS_Product_Calculated_Fields
ALTER TABLE dbo.LoanPASS_Product_Calculated_Fields
ADD Run_Id VARCHAR(50);

-- Add Run_Id to dbo.LoanPASS_Price_Scenarios
ALTER TABLE dbo.LoanPASS_Price_Scenarios
ADD Run_Id VARCHAR(50);

-- Add Run_Id to dbo.LoanPASS_Price_Scenario_Calculated_Fields
ALTER TABLE dbo.LoanPASS_Price_Scenario_Calculated_Fields
ADD Run_Id VARCHAR(50);

-- Add Run_Id to dbo.LoanPASS_Price_Scenario_Errors
ALTER TABLE dbo.LoanPASS_Price_Scenario_Errors
ADD Run_Id VARCHAR(50);

-- Add Run_Id to dbo.LoanPASS_Price_Scenario_Rejections
ALTER TABLE dbo.LoanPASS_Price_Scenario_Rejections
ADD Run_Id VARCHAR(50);

-- Add Run_Id to dbo.LoanPASS_Price_Scenario_Review_Requirements
ALTER TABLE dbo.LoanPASS_Price_Scenario_Review_Requirements
ADD Run_Id VARCHAR(50);

-- Add Run_Id to dbo.LoanPASS_Price_Scenario_Adjustments
ALTER TABLE dbo.LoanPASS_Price_Scenario_Adjustments
ADD Run_Id VARCHAR(50);

-- Add Run_Id to dbo.LoanPASS_Price_Scenario_Stipulations
ALTER TABLE dbo.LoanPASS_Price_Scenario_Stipulations
ADD Run_Id VARCHAR(50);

-- Alter Run_Id to VARCHAR(64) in dbo.LoanPASS_Product_Offerings
ALTER TABLE dbo.LoanPASS_Product_Offerings
ALTER COLUMN Run_Id VARCHAR(64);

-- Alter Run_Id to VARCHAR(64) in dbo.LoanPASS_Product_Calculated_Fields
ALTER TABLE dbo.LoanPASS_Product_Calculated_Fields
ALTER COLUMN Run_Id VARCHAR(64);

-- Alter Run_Id to VARCHAR(64) in dbo.LoanPASS_Price_Scenarios
ALTER TABLE dbo.LoanPASS_Price_Scenarios
ALTER COLUMN Run_Id VARCHAR(64);

-- Alter Run_Id to VARCHAR(64) in dbo.LoanPASS_Price_Scenario_Calculated_Fields
ALTER TABLE dbo.LoanPASS_Price_Scenario_Calculated_Fields
ALTER COLUMN Run_Id VARCHAR(64);

-- Alter Run_Id to VARCHAR(64) in dbo.LoanPASS_Price_Scenario_Errors
ALTER TABLE dbo.LoanPASS_Price_Scenario_Errors
ALTER COLUMN Run_Id VARCHAR(64);

-- Alter Run_Id to VARCHAR(64) in dbo.LoanPASS_Price_Scenario_Rejections
ALTER TABLE dbo.LoanPASS_Price_Scenario_Rejections
ALTER COLUMN Run_Id VARCHAR(64);

-- Alter Run_Id to VARCHAR(64) in dbo.LoanPASS_Price_Scenario_Review_Requirements
ALTER TABLE dbo.LoanPASS_Price_Scenario_Review_Requirements
ALTER COLUMN Run_Id VARCHAR(64);

-- Alter Run_Id to VARCHAR(64) in dbo.LoanPASS_Price_Scenario_Adjustments
ALTER TABLE dbo.LoanPASS_Price_Scenario_Adjustments
ALTER COLUMN Run_Id VARCHAR(64);

-- Alter Run_Id to VARCHAR(64) in dbo.LoanPASS_Price_Scenario_Stipulations
ALTER TABLE dbo.LoanPASS_Price_Scenario_Stipulations
ALTER COLUMN Run_Id VARCHAR(64);

drop index IX_UQ_Scenario_Business_Id_Filtered on dbo.LoanPASS_Price_Scenarios

PRINT 'Schema script finished.';

-- If the table might already exist and you want to redefine it,
-- you can uncomment the DROP TABLE statement below.
-- CAUTION: This will delete all existing data in the table!
-- DROP TABLE IF EXISTS dbo.slack_openai_map;

-- CREATE TABLE dbo.slack_openai_map (
--     slack_ts NVARCHAR(20) NOT NULL, -- Removed PRIMARY KEY
--     openai_thread NVARCHAR(255) NOT NULL, -- Removed UNIQUE
--     created_at DATETIME2 DEFAULT GETDATE() -- New timestamp field, defaults to current date/time on insert
-- );

-- -- Create a non-clustered index on the slack_ts column
-- CREATE INDEX IX_slack_openai_map_slack_ts
-- ON dbo.slack_openai_map (slack_ts);

-- ALTER TABLE dbo.slack_openai_map
-- ADD category NVARCHAR(255) DEFAULT 'General';

-- ALTER TABLE dbo.slack_openai_map
-- ALTER COLUMN category NVARCHAR(64);

-- ALTER TABLE dbo.slack_openai_map
-- ADD recipient NVARCHAR(64) DEFAULT 'recipient';

-- ALTER TABLE dbo.slack_openai_map
-- ADD recipient_email NVARCHAR(255) DEFAULT 'recipient@lendzfinancial.com';

-- ALTER TABLE dbo.slack_openai_map
-- ADD successful BIT DEFAULT 0;


-- ALTER TABLE dbo.slack_openai_map
-- ADD CONSTRAINT PK_slack_openai_map PRIMARY KEY (slack_ts);

-- ALTER TABLE dbo.slack_openai_map
-- ADD is_rated BIT DEFAULT 0;

-- EXEC sp_rename 'dbo.slack_openai_map.successful', 'is_successful', 'COLUMN';

TRUNCATE TABLE DBO.LoanPASS_Price_Scenario_Adjustments
TRUNCATE TABLE DBO.LoanPASS_Price_Scenario_Calculated_Fields
TRUNCATE TABLE DBO.LoanPASS_Price_Scenario_Errors   
TRUNCATE TABLE DBO.LoanPASS_Price_Scenario_Rejections
TRUNCATE TABLE DBO.LoanPASS_Price_Scenario_Review_Requirements  
TRUNCATE TABLE DBO.LoanPASS_Price_Scenario_Stipulations
TRUNCATE TABLE DBO.LoanPASS_Product_Calculated_Fields
-- Delete rows from table 'DBO.LoanPASS_Product_Offerings
DELETE FROM DBO.LoanPASS_Price_Scenarios
DELETE FROM DBO.LoanPASS_Product_Offerings


DECLARE @sql NVARCHAR(MAX) = N'';
SELECT @sql += 
    'SELECT ''' + s.name + '.' + t.name + ''' AS TableName, COUNT(*) AS RecordCount FROM [' + s.name + '].[' + t.name + '] UNION ALL '
FROM sys.tables t
JOIN sys.schemas s ON t.schema_id = s.schema_id
WHERE s.name = 'dbo' AND t.name LIKE 'LoanPass%';

-- Remove the last 'UNION ALL'
SET @sql = LEFT(@sql, LEN(@sql) - 10);
-- Execute the dynamic SQL
EXEC sp_executesql @sql;
