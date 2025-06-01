-- Table: dbo.LoanPASS_Product_Offerings
-- Represents the main Product Offering object.
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

---

-- Table: dbo.LoanPASS_Product_Calculated_Fields
-- Stores calculated fields associated with a Product Offering.
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
    Number_Value__c DECIMAL(18,2) NULL,
    String_Value__c NVARCHAR(255) NULL,
    Duration_Count__c DECIMAL(18,0) NULL,
    Duration_Unit__c NVARCHAR(255) NULL,

    -- Foreign Key Constraint
    CONSTRAINT FK_ProductCalculatedFields_ProductOfferings
        FOREIGN KEY (LoanPASS_Product_Offering_Id)
        REFERENCES dbo.LoanPASS_Product_Offerings(Id)
);

---

-- Table: dbo.LoanPASS_Price_Scenarios
-- Represents a specific pricing scenario for a Product Offering.
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

    -- Foreign Key Constraint
    CONSTRAINT FK_PriceScenarios_ProductOfferings
        FOREIGN KEY (LoanPASS_Product_Offering_Id)
        REFERENCES dbo.LoanPASS_Product_Offerings(Id)
);

---

-- Table: dbo.LoanPASS_Price_Scenario_Calculated_Fields
-- Stores calculated fields specific to a Price Scenario.
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
    Number_Value__c DECIMAL(18,2) NULL,
    String_Value__c NVARCHAR(255) NULL,
    Duration_Count__c DECIMAL(18,0) NULL,
    Duration_Unit__c NVARCHAR(255) NULL,

    -- Foreign Key Constraint
    CONSTRAINT FK_PSCalculatedFields_PriceScenarios
        FOREIGN KEY (LoanPASS_Price_Scenario_Id)
        REFERENCES dbo.LoanPASS_Price_Scenarios(Id)
);

---

-- Table: dbo.LoanPASS_Price_Scenario_Errors
-- Stores error details for a Price Scenario.
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
    Source_Type__c NVARCHAR(255) NULL,
    Source_Rule_Id__c NVARCHAR(255) NULL,
    Error_Type__c NVARCHAR(255) NULL,
    Error_Field_Id__c NVARCHAR(255) NULL,

    -- Foreign Key Constraint
    CONSTRAINT FK_PSErrors_PriceScenarios
        FOREIGN KEY (LoanPASS_Price_Scenario_Id)
        REFERENCES dbo.LoanPASS_Price_Scenarios(Id)
);

-- If the table might already exist and you want to redefine it,
-- you can uncomment the DROP TABLE statement below.
-- CAUTION: This will delete all existing data in the table!
-- DROP TABLE IF EXISTS dbo.slack_openai_map;

CREATE TABLE dbo.slack_openai_map (
    slack_ts NVARCHAR(20) NOT NULL, -- Removed PRIMARY KEY
    openai_thread NVARCHAR(255) NOT NULL, -- Removed UNIQUE
    created_at DATETIME2 DEFAULT GETDATE() -- New timestamp field, defaults to current date/time on insert
);

-- Create a non-clustered index on the slack_ts column
CREATE INDEX IX_slack_openai_map_slack_ts
ON dbo.slack_openai_map (slack_ts);

ALTER TABLE dbo.slack_openai_map
ADD category NVARCHAR(255) DEFAULT 'General';

ALTER TABLE dbo.slack_openai_map
ALTER COLUMN category NVARCHAR(64);

ALTER TABLE dbo.slack_openai_map
ADD recipient NVARCHAR(64) DEFAULT 'recipient';

ALTER TABLE dbo.slack_openai_map
ADD recipient_email NVARCHAR(255) DEFAULT 'recipient@lendzfinancial.com';

ALTER TABLE dbo.slack_openai_map
ADD successful BIT DEFAULT 0;


ALTER TABLE dbo.slack_openai_map
ADD CONSTRAINT PK_slack_openai_map PRIMARY KEY (slack_ts);

ALTER TABLE dbo.slack_openai_map
ADD is_rated BIT DEFAULT 0;

EXEC sp_rename 'dbo.slack_openai_map.successful', 'is_successful', 'COLUMN';
