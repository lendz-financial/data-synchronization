-- Declare variables to hold the generated IDs
DECLARE @ProductOfferingId INT;
DECLARE @PriceScenarioId INT;

-- Start a transaction for atomicity
BEGIN TRANSACTION;

-- 1. Insert into dbo.LoanPASS_Product_Offerings
INSERT INTO dbo.LoanPASS_Product_Offerings (
    Product_Id__c,
    Product_Name__c,
    Product_Code__c,
    Investor_Name__c,
    Investor_Code__c,
    Is_Pricing_Enabled__c,
    Status__c,
    Rate_Sheet_Effective_Timestamp__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    '39948',                                   -- Product_Id__c
    'DSCR 30 Year Fixed',                      -- Product_Name__c
    'OBFCDSCRPF30',                            -- Product_Code__c
    'Series 6',                                -- Investor_Name__c
    'OBFC',                                    -- Investor_Code__c
    1,                                         -- Is_Pricing_Enabled__c (true)
    'ok',                                      -- Status__c
    '2025-05-27T13:36:13.094011Z',             -- Rate_Sheet_Effective_Timestamp__c
    NULL,                                      -- Name (Salesforce AutoNumber, not applicable here)
    GETUTCDATE(),                              -- CreatedDate
    GETUTCDATE(),                              -- LastModifiedDate
    0                                          -- IsDeleted
);

-- Get the ID of the newly inserted Product Offering
SET @ProductOfferingId = SCOPE_IDENTITY();
PRINT 'Inserted into dbo.LoanPASS_Product_Offerings with Id: ' + CAST(@ProductOfferingId AS NVARCHAR(10));

-- 2. Insert into dbo.LoanPASS_Product_Calculated_Fields
-- For 'calc@amortization-type-allowed'
INSERT INTO dbo.LoanPASS_Product_Calculated_Fields (
    LoanPASS_Product_Offering_Id,
    Field_Id__c,
    Value_Type__c,
    Enum_Type_Id__c,
    Variant_Id__c,
    Number_Value__c,
    String_Value__c,
    Duration_Count__c,
    Duration_Unit__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @ProductOfferingId,
    'calc@amortization-type-allowed',
    'enum',
    'yes-no',
    'yes',
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);

-- For 'calc@total-lien-balance' (null value)
INSERT INTO dbo.LoanPASS_Product_Calculated_Fields (
    LoanPASS_Product_Offering_Id,
    Field_Id__c,
    Value_Type__c,
    Enum_Type_Id__c,
    Variant_Id__c,
    Number_Value__c,
    String_Value__c,
    Duration_Count__c,
    Duration_Unit__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @ProductOfferingId,
    'calc@total-lien-balance',
    'null', -- Explicitly set type as 'null' if the JSON indicates it
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);

-- For 'calc@months-since-chapter-7-bankruptcy' (null value)
INSERT INTO dbo.LoanPASS_Product_Calculated_Fields (
    LoanPASS_Product_Offering_Id,
    Field_Id__c,
    Value_Type__c,
    Enum_Type_Id__c,
    Variant_Id__c,
    Number_Value__c,
    String_Value__c,
    Duration_Count__c,
    Duration_Unit__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @ProductOfferingId,
    'calc@months-since-chapter-7-bankruptcy',
    'null',
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);

-- For 'calc@total-loan-amount'
INSERT INTO dbo.LoanPASS_Product_Calculated_Fields (
    LoanPASS_Product_Offering_Id,
    Field_Id__c,
    Value_Type__c,
    Enum_Type_Id__c,
    Variant_Id__c,
    Number_Value__c,
    String_Value__c,
    Duration_Count__c,
    Duration_Unit__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @ProductOfferingId,
    'calc@total-loan-amount',
    'number',
    NULL,
    NULL,
    450000.00,
    NULL,
    NULL,
    NULL,
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);

-- For 'calc@months-since-chapter-11-bankruptcy' (null value)
INSERT INTO dbo.LoanPASS_Product_Calculated_Fields (
    LoanPASS_Product_Offering_Id,
    Field_Id__c,
    Value_Type__c,
    Enum_Type_Id__c,
    Variant_Id__c,
    Number_Value__c,
    String_Value__c,
    Duration_Count__c,
    Duration_Unit__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @ProductOfferingId,
    'calc@months-since-chapter-11-bankruptcy',
    'null',
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);

-- For 'calc-field@obfc-state-tier'
INSERT INTO dbo.LoanPASS_Product_Calculated_Fields (
    LoanPASS_Product_Offering_Id,
    Field_Id__c,
    Value_Type__c,
    Enum_Type_Id__c,
    Variant_Id__c,
    Number_Value__c,
    String_Value__c,
    Duration_Count__c,
    Duration_Unit__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @ProductOfferingId,
    'calc-field@obfc-state-tier',
    'string',
    NULL,
    NULL,
    NULL,
    'Tier 1',
    NULL,
    NULL,
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);

-- For 'calc@months-since-short-sale' (null value)
INSERT INTO dbo.LoanPASS_Product_Calculated_Fields (
    LoanPASS_Product_Offering_Id,
    Field_Id__c,
    Value_Type__c,
    Enum_Type_Id__c,
    Variant_Id__c,
    Number_Value__c,
    String_Value__c,
    Duration_Count__c,
    Duration_Unit__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @ProductOfferingId,
    'calc@months-since-short-sale',
    'null',
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);

-- For 'calc@loan-term'
INSERT INTO dbo.LoanPASS_Product_Calculated_Fields (
    LoanPASS_Product_Offering_Id,
    Field_Id__c,
    Value_Type__c,
    Enum_Type_Id__c,
    Variant_Id__c,
    Number_Value__c,
    String_Value__c,
    Duration_Count__c,
    Duration_Unit__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @ProductOfferingId,
    'calc@loan-term',
    'duration',
    NULL,
    NULL,
    NULL,
    NULL,
    360,
    'months',
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);

-- For 'calc@months-since-chapter-13-bankruptcy' (null value)
INSERT INTO dbo.LoanPASS_Product_Calculated_Fields (
    LoanPASS_Product_Offering_Id,
    Field_Id__c,
    Value_Type__c,
    Enum_Type_Id__c,
    Variant_Id__c,
    Number_Value__c,
    String_Value__c,
    Duration_Count__c,
    Duration_Unit__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @ProductOfferingId,
    'calc@months-since-chapter-13-bankruptcy',
    'null',
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);

-- For 'calc@lien-position-allowed'
INSERT INTO dbo.LoanPASS_Product_Calculated_Fields (
    LoanPASS_Product_Offering_Id,
    Field_Id__c,
    Value_Type__c,
    Enum_Type_Id__c,
    Variant_Id__c,
    Number_Value__c,
    String_Value__c,
    Duration_Count__c,
    Duration_Unit__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @ProductOfferingId,
    'calc@lien-position-allowed',
    'enum',
    'yes-no',
    'yes',
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);

-- For 'calc@second-lien-cltv'
INSERT INTO dbo.LoanPASS_Product_Calculated_Fields (
    LoanPASS_Product_Offering_Id,
    Field_Id__c,
    Value_Type__c,
    Enum_Type_Id__c,
    Variant_Id__c,
    Number_Value__c,
    String_Value__c,
    Duration_Count__c,
    Duration_Unit__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @ProductOfferingId,
    'calc@second-lien-cltv',
    'number',
    NULL,
    NULL,
    0.00,
    NULL,
    NULL,
    NULL,
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);

-- For 'calc@months-since-foreclosure' (null value)
INSERT INTO dbo.LoanPASS_Product_Calculated_Fields (
    LoanPASS_Product_Offering_Id,
    Field_Id__c,
    Value_Type__c,
    Enum_Type_Id__c,
    Variant_Id__c,
    Number_Value__c,
    String_Value__c,
    Duration_Count__c,
    Duration_Unit__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @ProductOfferingId,
    'calc@months-since-foreclosure',
    'null',
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);

-- For 'calc@months-since-deed-in-lieu' (null value)
INSERT INTO dbo.LoanPASS_Product_Calculated_Fields (
    LoanPASS_Product_Offering_Id,
    Field_Id__c,
    Value_Type__c,
    Enum_Type_Id__c,
    Variant_Id__c,
    Number_Value__c,
    String_Value__c,
    Duration_Count__c,
    Duration_Unit__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @ProductOfferingId,
    'calc@months-since-deed-in-lieu',
    'null',
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);

-- For 'calc@ltv'
INSERT INTO dbo.LoanPASS_Product_Calculated_Fields (
    LoanPASS_Product_Offering_Id,
    Field_Id__c,
    Value_Type__c,
    Enum_Type_Id__c,
    Variant_Id__c,
    Number_Value__c,
    String_Value__c,
    Duration_Count__c,
    Duration_Unit__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @ProductOfferingId,
    'calc@ltv',
    'number',
    NULL,
    NULL,
    45.00,
    NULL,
    NULL,
    NULL,
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);

-- For 'calc@months-since-forbearance' (null value)
INSERT INTO dbo.LoanPASS_Product_Calculated_Fields (
    LoanPASS_Product_Offering_Id,
    Field_Id__c,
    Value_Type__c,
    Enum_Type_Id__c,
    Variant_Id__c,
    Number_Value__c,
    String_Value__c,
    Duration_Count__c,
    Duration_Unit__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @ProductOfferingId,
    'calc@months-since-forbearance',
    'null',
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);

PRINT 'Inserted Product Calculated Fields.';

-- 3. Insert into dbo.LoanPASS_Price_Scenarios and related tables
-- Scenario 1: id: 592057f9f9ed6a0e9758fefa412a3ea1
INSERT INTO dbo.LoanPASS_Price_Scenarios (
    LoanPASS_Product_Offering_Id,
    Adjusted_Rate__c,
    Adjusted_Price__c,
    Adjusted_Rate_Lock_Count__c,
    Adjusted_Rate_Lock_Unit__c,
    Undiscounted_Rate__c,
    Starting_Adjusted_Rate__c,
    Starting_Adjusted_Price__c,
    Status__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @ProductOfferingId,
    11.500,
    NULL,
    30,
    'days',
    NULL,
    NULL,
    NULL,
    'error',
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);
SET @PriceScenarioId = SCOPE_IDENTITY();
PRINT 'Inserted Price Scenario with Id: ' + CAST(@PriceScenarioId AS NVARCHAR(10));

-- Insert Calculated Fields for Price Scenario 1
INSERT INTO dbo.LoanPASS_Price_Scenario_Calculated_Fields (
    LoanPASS_Price_Scenario_Id,
    Field_Id__c,
    Value_Type__c,
    Enum_Type_Id__c,
    Variant_Id__c,
    Number_Value__c,
    String_Value__c,
    Duration_Count__c,
    Duration_Unit__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES
    (@PriceScenarioId, 'calc@adjusted-rate-lock-period', 'duration', NULL, NULL, NULL, NULL, 30, 'days', NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc-field@sgcp-investor-connect-refinance-matrix-output', 'null', NULL, NULL, NULL, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc-field@sgcp-investor-connect-purchase-matrix-output', 'null', NULL, NULL, NULL, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@final-interest-rate', 'number', NULL, NULL, 11.5, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@mtg-payment', 'number', NULL, NULL, 4456.32, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0);
PRINT 'Inserted Calculated Fields for Price Scenario 1.';

-- Insert Errors for Price Scenario 1
INSERT INTO dbo.LoanPASS_Price_Scenario_Errors (
    LoanPASS_Price_Scenario_Id,
    Source_Type__c,
    Source_Rule_Id__c,
    Error_Type__c,
    Error_Field_Id__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @PriceScenarioId,
    'rule',
    '84351',
    'blank-field',
    'field@decision-credit-score',
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);
PRINT 'Inserted Errors for Price Scenario 1.';

-- Scenario 2: id: ec7b2cf6bca4d7dec958a9dfda091daa
INSERT INTO dbo.LoanPASS_Price_Scenarios (
    LoanPASS_Product_Offering_Id,
    Adjusted_Rate__c,
    Adjusted_Price__c,
    Adjusted_Rate_Lock_Count__c,
    Adjusted_Rate_Lock_Unit__c,
    Undiscounted_Rate__c,
    Starting_Adjusted_Rate__c,
    Starting_Adjusted_Price__c,
    Status__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @ProductOfferingId,
    11.375,
    NULL,
    30,
    'days',
    NULL,
    NULL,
    NULL,
    'error',
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);
SET @PriceScenarioId = SCOPE_IDENTITY();
PRINT 'Inserted Price Scenario with Id: ' + CAST(@PriceScenarioId AS NVARCHAR(10));

-- Insert Calculated Fields for Price Scenario 2
INSERT INTO dbo.LoanPASS_Price_Scenario_Calculated_Fields (
    LoanPASS_Price_Scenario_Id,
    Field_Id__c,
    Value_Type__c,
    Enum_Type_Id__c,
    Variant_Id__c,
    Number_Value__c,
    String_Value__c,
    Duration_Count__c,
    Duration_Unit__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES
    (@PriceScenarioId, 'calc-field@sgcp-investor-connect-purchase-matrix-output', 'null', NULL, NULL, NULL, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@final-interest-rate', 'number', NULL, NULL, 11.375, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc-field@sgcp-investor-connect-refinance-matrix-output', 'null', NULL, NULL, NULL, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@mtg-payment', 'number', NULL, NULL, 4413.45, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@adjusted-rate-lock-period', 'duration', NULL, NULL, NULL, NULL, 30, 'days', NULL, GETUTCDATE(), GETUTCDATE(), 0);
PRINT 'Inserted Calculated Fields for Price Scenario 2.';

-- Insert Errors for Price Scenario 2
INSERT INTO dbo.LoanPASS_Price_Scenario_Errors (
    LoanPASS_Price_Scenario_Id,
    Source_Type__c,
    Source_Rule_Id__c,
    Error_Type__c,
    Error_Field_Id__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @PriceScenarioId,
    'rule',
    '84351',
    'blank-field',
    'field@decision-credit-score',
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);
PRINT 'Inserted Errors for Price Scenario 2.';

-- Scenario 3: id: a031ddc8fd6784da917269a1f6eb3770
INSERT INTO dbo.LoanPASS_Price_Scenarios (
    LoanPASS_Product_Offering_Id,
    Adjusted_Rate__c,
    Adjusted_Price__c,
    Adjusted_Rate_Lock_Count__c,
    Adjusted_Rate_Lock_Unit__c,
    Undiscounted_Rate__c,
    Starting_Adjusted_Rate__c,
    Starting_Adjusted_Price__c,
    Status__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @ProductOfferingId,
    11.250,
    NULL,
    30,
    'days',
    NULL,
    NULL,
    NULL,
    'error',
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);
SET @PriceScenarioId = SCOPE_IDENTITY();
PRINT 'Inserted Price Scenario with Id: ' + CAST(@PriceScenarioId AS NVARCHAR(10));

-- Insert Calculated Fields for Price Scenario 3
INSERT INTO dbo.LoanPASS_Price_Scenario_Calculated_Fields (
    LoanPASS_Price_Scenario_Id,
    Field_Id__c,
    Value_Type__c,
    Enum_Type_Id__c,
    Variant_Id__c,
    Number_Value__c,
    String_Value__c,
    Duration_Count__c,
    Duration_Unit__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES
    (@PriceScenarioId, 'calc-field@sgcp-investor-connect-purchase-matrix-output', 'null', NULL, NULL, NULL, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@adjusted-rate-lock-period', 'duration', NULL, NULL, NULL, NULL, 30, 'days', NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc-field@sgcp-investor-connect-refinance-matrix-output', 'null', NULL, NULL, NULL, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@final-interest-rate', 'number', NULL, NULL, 11.25, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@mtg-payment', 'number', NULL, NULL, 4370.68, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0);
PRINT 'Inserted Calculated Fields for Price Scenario 3.';

-- Insert Errors for Price Scenario 3
INSERT INTO dbo.LoanPASS_Price_Scenario_Errors (
    LoanPASS_Price_Scenario_Id,
    Source_Type__c,
    Source_Rule_Id__c,
    Error_Type__c,
    Error_Field_Id__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @PriceScenarioId,
    'rule',
    '84351',
    'blank-field',
    'field@decision-credit-score',
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);
PRINT 'Inserted Errors for Price Scenario 3.';

-- Scenario 4: id: bbe4a0999a8a72fff2e7eac9283dee8c
INSERT INTO dbo.LoanPASS_Price_Scenarios (
    LoanPASS_Product_Offering_Id,
    Adjusted_Rate__c,
    Adjusted_Price__c,
    Adjusted_Rate_Lock_Count__c,
    Adjusted_Rate_Lock_Unit__c,
    Undiscounted_Rate__c,
    Starting_Adjusted_Rate__c,
    Starting_Adjusted_Price__c,
    Status__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @ProductOfferingId,
    11.125,
    NULL,
    30,
    'days',
    NULL,
    NULL,
    NULL,
    'error',
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);
SET @PriceScenarioId = SCOPE_IDENTITY();
PRINT 'Inserted Price Scenario with Id: ' + CAST(@PriceScenarioId AS NVARCHAR(10));

-- Insert Calculated Fields for Price Scenario 4
INSERT INTO dbo.LoanPASS_Price_Scenario_Calculated_Fields (
    LoanPASS_Price_Scenario_Id,
    Field_Id__c,
    Value_Type__c,
    Enum_Type_Id__c,
    Variant_Id__c,
    Number_Value__c,
    String_Value__c,
    Duration_Count__c,
    Duration_Unit__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES
    (@PriceScenarioId, 'calc@final-interest-rate', 'number', NULL, NULL, 11.125, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc-field@sgcp-investor-connect-refinance-matrix-output', 'null', NULL, NULL, NULL, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@mtg-payment', 'number', NULL, NULL, 4328.02, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@adjusted-rate-lock-period', 'duration', NULL, NULL, NULL, NULL, 30, 'days', NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc-field@sgcp-investor-connect-purchase-matrix-output', 'null', NULL, NULL, NULL, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0);
PRINT 'Inserted Calculated Fields for Price Scenario 4.';

-- Insert Errors for Price Scenario 4
INSERT INTO dbo.LoanPASS_Price_Scenario_Errors (
    LoanPASS_Price_Scenario_Id,
    Source_Type__c,
    Source_Rule_Id__c,
    Error_Type__c,
    Error_Field_Id__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @PriceScenarioId,
    'rule',
    '84351',
    'blank-field',
    'field@decision-credit-score',
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);
PRINT 'Inserted Errors for Price Scenario 4.';

-- Scenario 5: id: 7a41679b6b2e0621c8c75ed8e3c2ae3a
INSERT INTO dbo.LoanPASS_Price_Scenarios (
    LoanPASS_Product_Offering_Id,
    Adjusted_Rate__c,
    Adjusted_Price__c,
    Adjusted_Rate_Lock_Count__c,
    Adjusted_Rate_Lock_Unit__c,
    Undiscounted_Rate__c,
    Starting_Adjusted_Rate__c,
    Starting_Adjusted_Price__c,
    Status__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @ProductOfferingId,
    11.000,
    NULL,
    30,
    'days',
    NULL,
    NULL,
    NULL,
    'error',
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);
SET @PriceScenarioId = SCOPE_IDENTITY();
PRINT 'Inserted Price Scenario with Id: ' + CAST(@PriceScenarioId AS NVARCHAR(10));

-- Insert Calculated Fields for Price Scenario 5
INSERT INTO dbo.LoanPASS_Price_Scenario_Calculated_Fields (
    LoanPASS_Price_Scenario_Id,
    Field_Id__c,
    Value_Type__c,
    Enum_Type_Id__c,
    Variant_Id__c,
    Number_Value__c,
    String_Value__c,
    Duration_Count__c,
    Duration_Unit__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES
    (@PriceScenarioId, 'calc@adjusted-rate-lock-period', 'duration', NULL, NULL, NULL, NULL, 30, 'days', NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc-field@sgcp-investor-connect-refinance-matrix-output', 'null', NULL, NULL, NULL, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc-field@sgcp-investor-connect-purchase-matrix-output', 'null', NULL, NULL, NULL, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@mtg-payment', 'number', NULL, NULL, 4285.46, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@final-interest-rate', 'number', NULL, NULL, 11.00, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0);
PRINT 'Inserted Calculated Fields for Price Scenario 5.';

-- Insert Errors for Price Scenario 5
INSERT INTO dbo.LoanPASS_Price_Scenario_Errors (
    LoanPASS_Price_Scenario_Id,
    Source_Type__c,
    Source_Rule_Id__c,
    Error_Type__c,
    Error_Field_Id__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @PriceScenarioId,
    'rule',
    '84351',
    'blank-field',
    'field@decision-credit-score',
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);
PRINT 'Inserted Errors for Price Scenario 5.';

-- Scenario 6: id: 0786e7dd066b09d524d88192ef7a8823
INSERT INTO dbo.LoanPASS_Price_Scenarios (
    LoanPASS_Product_Offering_Id,
    Adjusted_Rate__c,
    Adjusted_Price__c,
    Adjusted_Rate_Lock_Count__c,
    Adjusted_Rate_Lock_Unit__c,
    Undiscounted_Rate__c,
    Starting_Adjusted_Rate__c,
    Starting_Adjusted_Price__c,
    Status__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @ProductOfferingId,
    10.875,
    NULL,
    30,
    'days',
    NULL,
    NULL,
    NULL,
    'error',
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);
SET @PriceScenarioId = SCOPE_IDENTITY();
PRINT 'Inserted Price Scenario with Id: ' + CAST(@PriceScenarioId AS NVARCHAR(10));

-- Insert Calculated Fields for Price Scenario 6
INSERT INTO dbo.LoanPASS_Price_Scenario_Calculated_Fields (
    LoanPASS_Price_Scenario_Id,
    Field_Id__c,
    Value_Type__c,
    Enum_Type_Id__c,
    Variant_Id__c,
    Number_Value__c,
    String_Value__c,
    Duration_Count__c,
    Duration_Unit__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES
    (@PriceScenarioId, 'calc-field@sgcp-investor-connect-refinance-matrix-output', 'null', NULL, NULL, NULL, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@mtg-payment', 'number', NULL, NULL, 4243.01, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@final-interest-rate', 'number', NULL, NULL, 10.875, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc-field@sgcp-investor-connect-purchase-matrix-output', 'null', NULL, NULL, NULL, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@adjusted-rate-lock-period', 'duration', NULL, NULL, NULL, NULL, 30, 'days', NULL, GETUTCDATE(), GETUTCDATE(), 0);
PRINT 'Inserted Calculated Fields for Price Scenario 6.';

-- Insert Errors for Price Scenario 6
INSERT INTO dbo.LoanPASS_Price_Scenario_Errors (
    LoanPASS_Price_Scenario_Id,
    Source_Type__c,
    Source_Rule_Id__c,
    Error_Type__c,
    Error_Field_Id__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @PriceScenarioId,
    'rule',
    '84351',
    'blank-field',
    'field@decision-credit-score',
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);
PRINT 'Inserted Errors for Price Scenario 6.';

-- Scenario 7: id: 4d48c17793a6cf216aaa8ff36db7287d
INSERT INTO dbo.LoanPASS_Price_Scenarios (
    LoanPASS_Product_Offering_Id,
    Adjusted_Rate__c,
    Adjusted_Price__c,
    Adjusted_Rate_Lock_Count__c,
    Adjusted_Rate_Lock_Unit__c,
    Undiscounted_Rate__c,
    Starting_Adjusted_Rate__c,
    Starting_Adjusted_Price__c,
    Status__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @ProductOfferingId,
    10.750,
    NULL,
    30,
    'days',
    NULL,
    NULL,
    NULL,
    'error',
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);
SET @PriceScenarioId = SCOPE_IDENTITY();
PRINT 'Inserted Price Scenario with Id: ' + CAST(@PriceScenarioId AS NVARCHAR(10));

-- Insert Calculated Fields for Price Scenario 7
INSERT INTO dbo.LoanPASS_Price_Scenario_Calculated_Fields (
    LoanPASS_Price_Scenario_Id,
    Field_Id__c,
    Value_Type__c,
    Enum_Type_Id__c,
    Variant_Id__c,
    Number_Value__c,
    String_Value__c,
    Duration_Count__c,
    Duration_Unit__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES
    (@PriceScenarioId, 'calc@mtg-payment', 'number', NULL, NULL, 4200.67, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@final-interest-rate', 'number', NULL, NULL, 10.75, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc-field@sgcp-investor-connect-refinance-matrix-output', 'null', NULL, NULL, NULL, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc-field@sgcp-investor-connect-purchase-matrix-output', 'null', NULL, NULL, NULL, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@adjusted-rate-lock-period', 'duration', NULL, NULL, NULL, NULL, 30, 'days', NULL, GETUTCDATE(), GETUTCDATE(), 0);
PRINT 'Inserted Calculated Fields for Price Scenario 7.';

-- Insert Errors for Price Scenario 7
INSERT INTO dbo.LoanPASS_Price_Scenario_Errors (
    LoanPASS_Price_Scenario_Id,
    Source_Type__c,
    Source_Rule_Id__c,
    Error_Type__c,
    Error_Field_Id__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @PriceScenarioId,
    'rule',
    '84351',
    'blank-field',
    'field@decision-credit-score',
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);
PRINT 'Inserted Errors for Price Scenario 7.';

-- Scenario 8: id: fe7aa48e6706246620211340793ed3aa
INSERT INTO dbo.LoanPASS_Price_Scenarios (
    LoanPASS_Product_Offering_Id,
    Adjusted_Rate__c,
    Adjusted_Price__c,
    Adjusted_Rate_Lock_Count__c,
    Adjusted_Rate_Lock_Unit__c,
    Undiscounted_Rate__c,
    Starting_Adjusted_Rate__c,
    Starting_Adjusted_Price__c,
    Status__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @ProductOfferingId,
    10.625,
    NULL,
    30,
    'days',
    NULL,
    NULL,
    NULL,
    'error',
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);
SET @PriceScenarioId = SCOPE_IDENTITY();
PRINT 'Inserted Price Scenario with Id: ' + CAST(@PriceScenarioId AS NVARCHAR(10));

-- Insert Calculated Fields for Price Scenario 8
INSERT INTO dbo.LoanPASS_Price_Scenario_Calculated_Fields (
    LoanPASS_Price_Scenario_Id,
    Field_Id__c,
    Value_Type__c,
    Enum_Type_Id__c,
    Variant_Id__c,
    Number_Value__c,
    String_Value__c,
    Duration_Count__c,
    Duration_Unit__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES
    (@PriceScenarioId, 'calc-field@sgcp-investor-connect-refinance-matrix-output', 'null', NULL, NULL, NULL, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc-field@sgcp-investor-connect-purchase-matrix-output', 'null', NULL, NULL, NULL, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@mtg-payment', 'number', NULL, NULL, 4158.44, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@final-interest-rate', 'number', NULL, NULL, 10.625, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@adjusted-rate-lock-period', 'duration', NULL, NULL, NULL, NULL, 30, 'days', NULL, GETUTCDATE(), GETUTCDATE(), 0);
PRINT 'Inserted Calculated Fields for Price Scenario 8.';

-- Insert Errors for Price Scenario 8
INSERT INTO dbo.LoanPASS_Price_Scenario_Errors (
    LoanPASS_Price_Scenario_Id,
    Source_Type__c,
    Source_Rule_Id__c,
    Error_Type__c,
    Error_Field_Id__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @PriceScenarioId,
    'rule',
    '84351',
    'blank-field',
    'field@decision-credit-score',
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);
PRINT 'Inserted Errors for Price Scenario 8.';

-- Scenario 9: id: ea34d0f52280d15a7f0a447fa76cd44a
INSERT INTO dbo.LoanPASS_Price_Scenarios (
    LoanPASS_Product_Offering_Id,
    Adjusted_Rate__c,
    Adjusted_Price__c,
    Adjusted_Rate_Lock_Count__c,
    Adjusted_Rate_Lock_Unit__c,
    Undiscounted_Rate__c,
    Starting_Adjusted_Rate__c,
    Starting_Adjusted_Price__c,
    Status__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @ProductOfferingId,
    10.500,
    NULL,
    30,
    'days',
    NULL,
    NULL,
    NULL,
    'error',
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);
SET @PriceScenarioId = SCOPE_IDENTITY();
PRINT 'Inserted Price Scenario with Id: ' + CAST(@PriceScenarioId AS NVARCHAR(10));

-- Insert Calculated Fields for Price Scenario 9
INSERT INTO dbo.LoanPASS_Price_Scenario_Calculated_Fields (
    LoanPASS_Price_Scenario_Id,
    Field_Id__c,
    Value_Type__c,
    Enum_Type_Id__c,
    Variant_Id__c,
    Number_Value__c,
    String_Value__c,
    Duration_Count__c,
    Duration_Unit__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES
    (@PriceScenarioId, 'calc@final-interest-rate', 'number', NULL, NULL, 10.5, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@mtg-payment', 'number', NULL, NULL, 4116.33, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc-field@sgcp-investor-connect-purchase-matrix-output', 'null', NULL, NULL, NULL, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc-field@sgcp-investor-connect-refinance-matrix-output', 'null', NULL, NULL, NULL, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@adjusted-rate-lock-period', 'duration', NULL, NULL, NULL, NULL, 30, 'days', NULL, GETUTCDATE(), GETUTCDATE(), 0);
PRINT 'Inserted Calculated Fields for Price Scenario 9.';

-- Insert Errors for Price Scenario 9
INSERT INTO dbo.LoanPASS_Price_Scenario_Errors (
    LoanPASS_Price_Scenario_Id,
    Source_Type__c,
    Source_Rule_Id__c,
    Error_Type__c,
    Error_Field_Id__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @PriceScenarioId,
    'rule',
    '84351',
    'blank-field',
    'field@decision-credit-score',
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);
PRINT 'Inserted Errors for Price Scenario 9.';

-- Scenario 10: id: f2298a12ca262b18d5db2977c27c5560
INSERT INTO dbo.LoanPASS_Price_Scenarios (
    LoanPASS_Product_Offering_Id,
    Adjusted_Rate__c,
    Adjusted_Price__c,
    Adjusted_Rate_Lock_Count__c,
    Adjusted_Rate_Lock_Unit__c,
    Undiscounted_Rate__c,
    Starting_Adjusted_Rate__c,
    Starting_Adjusted_Price__c,
    Status__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @ProductOfferingId,
    10.375,
    NULL,
    30,
    'days',
    NULL,
    NULL,
    NULL,
    'error',
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);
SET @PriceScenarioId = SCOPE_IDENTITY();
PRINT 'Inserted Price Scenario with Id: ' + CAST(@PriceScenarioId AS NVARCHAR(10));

-- Insert Calculated Fields for Price Scenario 10
INSERT INTO dbo.LoanPASS_Price_Scenario_Calculated_Fields (
    LoanPASS_Price_Scenario_Id,
    Field_Id__c,
    Value_Type__c,
    Enum_Type_Id__c,
    Variant_Id__c,
    Number_Value__c,
    String_Value__c,
    Duration_Count__c,
    Duration_Unit__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES
    (@PriceScenarioId, 'calc-field@sgcp-investor-connect-refinance-matrix-output', 'null', NULL, NULL, NULL, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@mtg-payment', 'number', NULL, NULL, 4074.34, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@adjusted-rate-lock-period', 'duration', NULL, NULL, NULL, NULL, 30, 'days', NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@final-interest-rate', 'number', NULL, NULL, 10.375, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc-field@sgcp-investor-connect-purchase-matrix-output', 'null', NULL, NULL, NULL, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0);
PRINT 'Inserted Calculated Fields for Price Scenario 10.';

-- Insert Errors for Price Scenario 10
INSERT INTO dbo.LoanPASS_Price_Scenario_Errors (
    LoanPASS_Price_Scenario_Id,
    Source_Type__c,
    Source_Rule_Id__c,
    Error_Type__c,
    Error_Field_Id__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @PriceScenarioId,
    'rule',
    '84351',
    'blank-field',
    'field@decision-credit-score',
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);
PRINT 'Inserted Errors for Price Scenario 10.';

-- Scenario 11: id: c51f0b1ea0772307cffb925f8ee9a0be
INSERT INTO dbo.LoanPASS_Price_Scenarios (
    LoanPASS_Product_Offering_Id,
    Adjusted_Rate__c,
    Adjusted_Price__c,
    Adjusted_Rate_Lock_Count__c,
    Adjusted_Rate_Lock_Unit__c,
    Undiscounted_Rate__c,
    Starting_Adjusted_Rate__c,
    Starting_Adjusted_Price__c,
    Status__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @ProductOfferingId,
    10.250,
    NULL,
    30,
    'days',
    NULL,
    NULL,
    NULL,
    'error',
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);
SET @PriceScenarioId = SCOPE_IDENTITY();
PRINT 'Inserted Price Scenario with Id: ' + CAST(@PriceScenarioId AS NVARCHAR(10));

-- Insert Calculated Fields for Price Scenario 11
INSERT INTO dbo.LoanPASS_Price_Scenario_Calculated_Fields (
    LoanPASS_Price_Scenario_Id,
    Field_Id__c,
    Value_Type__c,
    Enum_Type_Id__c,
    Variant_Id__c,
    Number_Value__c,
    String_Value__c,
    Duration_Count__c,
    Duration_Unit__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES
    (@PriceScenarioId, 'calc-field@sgcp-investor-connect-refinance-matrix-output', 'null', NULL, NULL, NULL, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc-field@sgcp-investor-connect-purchase-matrix-output', 'null', NULL, NULL, NULL, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@mtg-payment', 'number', NULL, NULL, 4032.46, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@final-interest-rate', 'number', NULL, NULL, 10.25, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@adjusted-rate-lock-period', 'duration', NULL, NULL, NULL, NULL, 30, 'days', NULL, GETUTCDATE(), GETUTCDATE(), 0);
PRINT 'Inserted Calculated Fields for Price Scenario 11.';

-- Insert Errors for Price Scenario 11
INSERT INTO dbo.LoanPASS_Price_Scenario_Errors (
    LoanPASS_Price_Scenario_Id,
    Source_Type__c,
    Source_Rule_Id__c,
    Error_Type__c,
    Error_Field_Id__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @PriceScenarioId,
    'rule',
    '84351',
    'blank-field',
    'field@decision-credit-score',
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);
PRINT 'Inserted Errors for Price Scenario 11.';

-- Scenario 12: id: 6baccb1170c400ce17ed1db9be1e1027
INSERT INTO dbo.LoanPASS_Price_Scenarios (
    LoanPASS_Product_Offering_Id,
    Adjusted_Rate__c,
    Adjusted_Price__c,
    Adjusted_Rate_Lock_Count__c,
    Adjusted_Rate_Lock_Unit__c,
    Undiscounted_Rate__c,
    Starting_Adjusted_Rate__c,
    Starting_Adjusted_Price__c,
    Status__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @ProductOfferingId,
    10.125,
    NULL,
    30,
    'days',
    NULL,
    NULL,
    NULL,
    'error',
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);
SET @PriceScenarioId = SCOPE_IDENTITY();
PRINT 'Inserted Price Scenario with Id: ' + CAST(@PriceScenarioId AS NVARCHAR(10));

-- Insert Calculated Fields for Price Scenario 12
INSERT INTO dbo.LoanPASS_Price_Scenario_Calculated_Fields (
    LoanPASS_Price_Scenario_Id,
    Field_Id__c,
    Value_Type__c,
    Enum_Type_Id__c,
    Variant_Id__c,
    Number_Value__c,
    String_Value__c,
    Duration_Count__c,
    Duration_Unit__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES
    (@PriceScenarioId, 'calc-field@sgcp-investor-connect-refinance-matrix-output', 'null', NULL, NULL, NULL, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@final-interest-rate', 'number', NULL, NULL, 10.125, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@mtg-payment', 'number', NULL, NULL, 3990.71, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@adjusted-rate-lock-period', 'duration', NULL, NULL, NULL, NULL, 30, 'days', NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc-field@sgcp-investor-connect-purchase-matrix-output', 'null', NULL, NULL, NULL, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0);
PRINT 'Inserted Calculated Fields for Price Scenario 12.';

-- Insert Errors for Price Scenario 12
INSERT INTO dbo.LoanPASS_Price_Scenario_Errors (
    LoanPASS_Price_Scenario_Id,
    Source_Type__c,
    Source_Rule_Id__c,
    Error_Type__c,
    Error_Field_Id__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @PriceScenarioId,
    'rule',
    '84351',
    'blank-field',
    'field@decision-credit-score',
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);
PRINT 'Inserted Errors for Price Scenario 12.';

-- Scenario 13: id: 1b54c861b86179e3a783bacefab80dbd
INSERT INTO dbo.LoanPASS_Price_Scenarios (
    LoanPASS_Product_Offering_Id,
    Adjusted_Rate__c,
    Adjusted_Price__c,
    Adjusted_Rate_Lock_Count__c,
    Adjusted_Rate_Lock_Unit__c,
    Undiscounted_Rate__c,
    Starting_Adjusted_Rate__c,
    Starting_Adjusted_Price__c,
    Status__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @ProductOfferingId,
    10.000,
    NULL,
    30,
    'days',
    NULL,
    NULL,
    NULL,
    'error',
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);
SET @PriceScenarioId = SCOPE_IDENTITY();
PRINT 'Inserted Price Scenario with Id: ' + CAST(@PriceScenarioId AS NVARCHAR(10));

-- Insert Calculated Fields for Price Scenario 13
INSERT INTO dbo.LoanPASS_Price_Scenario_Calculated_Fields (
    LoanPASS_Price_Scenario_Id,
    Field_Id__c,
    Value_Type__c,
    Enum_Type_Id__c,
    Variant_Id__c,
    Number_Value__c,
    String_Value__c,
    Duration_Count__c,
    Duration_Unit__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES
    (@PriceScenarioId, 'calc@final-interest-rate', 'number', NULL, NULL, 10.00, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc-field@sgcp-investor-connect-refinance-matrix-output', 'null', NULL, NULL, NULL, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@mtg-payment', 'number', NULL, NULL, 3949.08, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc-field@sgcp-investor-connect-purchase-matrix-output', 'null', NULL, NULL, NULL, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@adjusted-rate-lock-period', 'duration', NULL, NULL, NULL, NULL, 30, 'days', NULL, GETUTCDATE(), GETUTCDATE(), 0);
PRINT 'Inserted Calculated Fields for Price Scenario 13.';

-- Insert Errors for Price Scenario 13
INSERT INTO dbo.LoanPASS_Price_Scenario_Errors (
    LoanPASS_Price_Scenario_Id,
    Source_Type__c,
    Source_Rule_Id__c,
    Error_Type__c,
    Error_Field_Id__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @PriceScenarioId,
    'rule',
    '84351',
    'blank-field',
    'field@decision-credit-score',
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);
PRINT 'Inserted Errors for Price Scenario 13.';

-- Scenario 14: id: 0f321dd91e6d7b8a593d058e2f1370de
INSERT INTO dbo.LoanPASS_Price_Scenarios (
    LoanPASS_Product_Offering_Id,
    Adjusted_Rate__c,
    Adjusted_Price__c,
    Adjusted_Rate_Lock_Count__c,
    Adjusted_Rate_Lock_Unit__c,
    Undiscounted_Rate__c,
    Starting_Adjusted_Rate__c,
    Starting_Adjusted_Price__c,
    Status__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @ProductOfferingId,
    9.875,
    NULL,
    30,
    'days',
    NULL,
    NULL,
    NULL,
    'error',
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);
SET @PriceScenarioId = SCOPE_IDENTITY();
PRINT 'Inserted Price Scenario with Id: ' + CAST(@PriceScenarioId AS NVARCHAR(10));

-- Insert Calculated Fields for Price Scenario 14
INSERT INTO dbo.LoanPASS_Price_Scenario_Calculated_Fields (
    LoanPASS_Price_Scenario_Id,
    Field_Id__c,
    Value_Type__c,
    Enum_Type_Id__c,
    Variant_Id__c,
    Number_Value__c,
    String_Value__c,
    Duration_Count__c,
    Duration_Unit__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES
    (@PriceScenarioId, 'calc@adjusted-rate-lock-period', 'duration', NULL, NULL, NULL, NULL, 30, 'days', NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@final-interest-rate', 'number', NULL, NULL, 9.875, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@mtg-payment', 'number', NULL, NULL, 3907.57, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc-field@sgcp-investor-connect-refinance-matrix-output', 'null', NULL, NULL, NULL, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc-field@sgcp-investor-connect-purchase-matrix-output', 'null', NULL, NULL, NULL, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0);
PRINT 'Inserted Calculated Fields for Price Scenario 14.';

-- Insert Errors for Price Scenario 14
INSERT INTO dbo.LoanPASS_Price_Scenario_Errors (
    LoanPASS_Price_Scenario_Id,
    Source_Type__c,
    Source_Rule_Id__c,
    Error_Type__c,
    Error_Field_Id__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @PriceScenarioId,
    'rule',
    '84351',
    'blank-field',
    'field@decision-credit-score',
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);
PRINT 'Inserted Errors for Price Scenario 14.';

-- Scenario 15: id: c2b87119166f2a57d5aa6999c04e34df
INSERT INTO dbo.LoanPASS_Price_Scenarios (
    LoanPASS_Product_Offering_Id,
    Adjusted_Rate__c,
    Adjusted_Price__c,
    Adjusted_Rate_Lock_Count__c,
    Adjusted_Rate_Lock_Unit__c,
    Undiscounted_Rate__c,
    Starting_Adjusted_Rate__c,
    Starting_Adjusted_Price__c,
    Status__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @ProductOfferingId,
    9.750,
    NULL,
    30,
    'days',
    NULL,
    NULL,
    NULL,
    'error',
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);
SET @PriceScenarioId = SCOPE_IDENTITY();
PRINT 'Inserted Price Scenario with Id: ' + CAST(@PriceScenarioId AS NVARCHAR(10));

-- Insert Calculated Fields for Price Scenario 15
INSERT INTO dbo.LoanPASS_Price_Scenario_Calculated_Fields (
    LoanPASS_Price_Scenario_Id,
    Field_Id__c,
    Value_Type__c,
    Enum_Type_Id__c,
    Variant_Id__c,
    Number_Value__c,
    String_Value__c,
    Duration_Count__c,
    Duration_Unit__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES
    (@PriceScenarioId, 'calc@adjusted-rate-lock-period', 'duration', NULL, NULL, NULL, NULL, 30, 'days', NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@mtg-payment', 'number', NULL, NULL, 3866.20, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc-field@sgcp-investor-connect-purchase-matrix-output', 'null', NULL, NULL, NULL, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc-field@sgcp-investor-connect-refinance-matrix-output', 'null', NULL, NULL, NULL, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@final-interest-rate', 'number', NULL, NULL, 9.75, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0);
PRINT 'Inserted Calculated Fields for Price Scenario 15.';

-- Insert Errors for Price Scenario 15
INSERT INTO dbo.LoanPASS_Price_Scenario_Errors (
    LoanPASS_Price_Scenario_Id,
    Source_Type__c,
    Source_Rule_Id__c,
    Error_Type__c,
    Error_Field_Id__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @PriceScenarioId,
    'rule',
    '84351',
    'blank-field',
    'field@decision-credit-score',
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);
PRINT 'Inserted Errors for Price Scenario 15.';

-- Scenario 16: id: f98e77e722769daaa4195d2ba136dfab
INSERT INTO dbo.LoanPASS_Price_Scenarios (
    LoanPASS_Product_Offering_Id,
    Adjusted_Rate__c,
    Adjusted_Price__c,
    Adjusted_Rate_Lock_Count__c,
    Adjusted_Rate_Lock_Unit__c,
    Undiscounted_Rate__c,
    Starting_Adjusted_Rate__c,
    Starting_Adjusted_Price__c,
    Status__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @ProductOfferingId,
    9.625,
    NULL,
    30,
    'days',
    NULL,
    NULL,
    NULL,
    'error',
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);
SET @PriceScenarioId = SCOPE_IDENTITY();
PRINT 'Inserted Price Scenario with Id: ' + CAST(@PriceScenarioId AS NVARCHAR(10));

-- Insert Calculated Fields for Price Scenario 16
INSERT INTO dbo.LoanPASS_Price_Scenario_Calculated_Fields (
    LoanPASS_Price_Scenario_Id,
    Field_Id__c,
    Value_Type__c,
    Enum_Type_Id__c,
    Variant_Id__c,
    Number_Value__c,
    String_Value__c,
    Duration_Count__c,
    Duration_Unit__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES
    (@PriceScenarioId, 'calc@mtg-payment', 'number', NULL, NULL, 3824.96, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc-field@sgcp-investor-connect-purchase-matrix-output', 'null', NULL, NULL, NULL, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc-field@sgcp-investor-connect-refinance-matrix-output', 'null', NULL, NULL, NULL, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@final-interest-rate', 'number', NULL, NULL, 9.625, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@adjusted-rate-lock-period', 'duration', NULL, NULL, NULL, NULL, 30, 'days', NULL, GETUTCDATE(), GETUTCDATE(), 0);
PRINT 'Inserted Calculated Fields for Price Scenario 16.';

-- Insert Errors for Price Scenario 16
INSERT INTO dbo.LoanPASS_Price_Scenario_Errors (
    LoanPASS_Price_Scenario_Id,
    Source_Type__c,
    Source_Rule_Id__c,
    Error_Type__c,
    Error_Field_Id__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @PriceScenarioId,
    'rule',
    '84351',
    'blank-field',
    'field@decision-credit-score',
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);
PRINT 'Inserted Errors for Price Scenario 16.';

-- Scenario 17: id: 7f5292977ad7b0a4a5c1e4ca09a2b10c
INSERT INTO dbo.LoanPASS_Price_Scenarios (
    LoanPASS_Product_Offering_Id,
    Adjusted_Rate__c,
    Adjusted_Price__c,
    Adjusted_Rate_Lock_Count__c,
    Adjusted_Rate_Lock_Unit__c,
    Undiscounted_Rate__c,
    Starting_Adjusted_Rate__c,
    Starting_Adjusted_Price__c,
    Status__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @ProductOfferingId,
    9.500,
    NULL,
    30,
    'days',
    NULL,
    NULL,
    NULL,
    'error',
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);
SET @PriceScenarioId = SCOPE_IDENTITY();
PRINT 'Inserted Price Scenario with Id: ' + CAST(@PriceScenarioId AS NVARCHAR(10));

-- Insert Calculated Fields for Price Scenario 17
INSERT INTO dbo.LoanPASS_Price_Scenario_Calculated_Fields (
    LoanPASS_Price_Scenario_Id,
    Field_Id__c,
    Value_Type__c,
    Enum_Type_Id__c,
    Variant_Id__c,
    Number_Value__c,
    String_Value__c,
    Duration_Count__c,
    Duration_Unit__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES
    (@PriceScenarioId, 'calc-field@sgcp-investor-connect-refinance-matrix-output', 'null', NULL, NULL, NULL, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc-field@sgcp-investor-connect-purchase-matrix-output', 'null', NULL, NULL, NULL, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@adjusted-rate-lock-period', 'duration', NULL, NULL, NULL, NULL, 30, 'days', NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@mtg-payment', 'number', NULL, NULL, 3783.85, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@final-interest-rate', 'number', NULL, NULL, 9.50, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0);
PRINT 'Inserted Calculated Fields for Price Scenario 17.';

-- Insert Errors for Price Scenario 17
INSERT INTO dbo.LoanPASS_Price_Scenario_Errors (
    LoanPASS_Price_Scenario_Id,
    Source_Type__c,
    Source_Rule_Id__c,
    Error_Type__c,
    Error_Field_Id__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @PriceScenarioId,
    'rule',
    '84351',
    'blank-field',
    'field@decision-credit-score',
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);
PRINT 'Inserted Errors for Price Scenario 17.';

-- Scenario 18: id: 1981f36c7048db0f7558c66310a5be52
INSERT INTO dbo.LoanPASS_Price_Scenarios (
    LoanPASS_Product_Offering_Id,
    Adjusted_Rate__c,
    Adjusted_Price__c,
    Adjusted_Rate_Lock_Count__c,
    Adjusted_Rate_Lock_Unit__c,
    Undiscounted_Rate__c,
    Starting_Adjusted_Rate__c,
    Starting_Adjusted_Price__c,
    Status__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @ProductOfferingId,
    9.375,
    NULL,
    30,
    'days',
    NULL,
    NULL,
    NULL,
    'error',
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);
SET @PriceScenarioId = SCOPE_IDENTITY();
PRINT 'Inserted Price Scenario with Id: ' + CAST(@PriceScenarioId AS NVARCHAR(10));

-- Insert Calculated Fields for Price Scenario 18
INSERT INTO dbo.LoanPASS_Price_Scenario_Calculated_Fields (
    LoanPASS_Price_Scenario_Id,
    Field_Id__c,
    Value_Type__c,
    Enum_Type_Id__c,
    Variant_Id__c,
    Number_Value__c,
    String_Value__c,
    Duration_Count__c,
    Duration_Unit__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES
    (@PriceScenarioId, 'calc@adjusted-rate-lock-period', 'duration', NULL, NULL, NULL, NULL, 30, 'days', NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc-field@sgcp-investor-connect-refinance-matrix-output', 'null', NULL, NULL, NULL, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc-field@sgcp-investor-connect-purchase-matrix-output', 'null', NULL, NULL, NULL, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@mtg-payment', 'number', NULL, NULL, 3742.88, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@final-interest-rate', 'number', NULL, NULL, 9.375, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0);
PRINT 'Inserted Calculated Fields for Price Scenario 18.';

-- Insert Errors for Price Scenario 18
INSERT INTO dbo.LoanPASS_Price_Scenario_Errors (
    LoanPASS_Price_Scenario_Id,
    Source_Type__c,
    Source_Rule_Id__c,
    Error_Type__c,
    Error_Field_Id__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @PriceScenarioId,
    'rule',
    '84351',
    'blank-field',
    'field@decision-credit-score',
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);
PRINT 'Inserted Errors for Price Scenario 18.';

-- Scenario 19: id: b1312e1bb869a13ba75c28c32ec4acb5
INSERT INTO dbo.LoanPASS_Price_Scenarios (
    LoanPASS_Product_Offering_Id,
    Adjusted_Rate__c,
    Adjusted_Price__c,
    Adjusted_Rate_Lock_Count__c,
    Adjusted_Rate_Lock_Unit__c,
    Undiscounted_Rate__c,
    Starting_Adjusted_Rate__c,
    Starting_Adjusted_Price__c,
    Status__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @ProductOfferingId,
    9.250,
    NULL,
    30,
    'days',
    NULL,
    NULL,
    NULL,
    'error',
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);
SET @PriceScenarioId = SCOPE_IDENTITY();
PRINT 'Inserted Price Scenario with Id: ' + CAST(@PriceScenarioId AS NVARCHAR(10));

-- Insert Calculated Fields for Price Scenario 19
INSERT INTO dbo.LoanPASS_Price_Scenario_Calculated_Fields (
    LoanPASS_Price_Scenario_Id,
    Field_Id__c,
    Value_Type__c,
    Enum_Type_Id__c,
    Variant_Id__c,
    Number_Value__c,
    String_Value__c,
    Duration_Count__c,
    Duration_Unit__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES
    (@PriceScenarioId, 'calc@final-interest-rate', 'number', NULL, NULL, 9.25, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc-field@sgcp-investor-connect-purchase-matrix-output', 'null', NULL, NULL, NULL, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc-field@sgcp-investor-connect-refinance-matrix-output', 'null', NULL, NULL, NULL, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@adjusted-rate-lock-period', 'duration', NULL, NULL, NULL, NULL, 30, 'days', NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@mtg-payment', 'number', NULL, NULL, 3702.04, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0);
PRINT 'Inserted Calculated Fields for Price Scenario 19.';

-- Insert Errors for Price Scenario 19
INSERT INTO dbo.LoanPASS_Price_Scenario_Errors (
    LoanPASS_Price_Scenario_Id,
    Source_Type__c,
    Source_Rule_Id__c,
    Error_Type__c,
    Error_Field_Id__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @PriceScenarioId,
    'rule',
    '84351',
    'blank-field',
    'field@decision-credit-score',
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);
PRINT 'Inserted Errors for Price Scenario 19.';

-- Scenario 20: id: a17a0aa0889e4c0875e82b7350654834
INSERT INTO dbo.LoanPASS_Price_Scenarios (
    LoanPASS_Product_Offering_Id,
    Adjusted_Rate__c,
    Adjusted_Price__c,
    Adjusted_Rate_Lock_Count__c,
    Adjusted_Rate_Lock_Unit__c,
    Undiscounted_Rate__c,
    Starting_Adjusted_Rate__c,
    Starting_Adjusted_Price__c,
    Status__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @ProductOfferingId,
    9.125,
    NULL,
    30,
    'days',
    NULL,
    NULL,
    NULL,
    'error',
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);
SET @PriceScenarioId = SCOPE_IDENTITY();
PRINT 'Inserted Price Scenario with Id: ' + CAST(@PriceScenarioId AS NVARCHAR(10));

-- Insert Calculated Fields for Price Scenario 20
INSERT INTO dbo.LoanPASS_Price_Scenario_Calculated_Fields (
    LoanPASS_Price_Scenario_Id,
    Field_Id__c,
    Value_Type__c,
    Enum_Type_Id__c,
    Variant_Id__c,
    Number_Value__c,
    String_Value__c,
    Duration_Count__c,
    Duration_Unit__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES
    (@PriceScenarioId, 'calc@adjusted-rate-lock-period', 'duration', NULL, NULL, NULL, NULL, 30, 'days', NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc-field@sgcp-investor-connect-purchase-matrix-output', 'null', NULL, NULL, NULL, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc-field@sgcp-investor-connect-refinance-matrix-output', 'null', NULL, NULL, NULL, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@final-interest-rate', 'number', NULL, NULL, 9.125, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@mtg-payment', 'number', NULL, NULL, 3661.35, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0);
PRINT 'Inserted Calculated Fields for Price Scenario 20.';

-- Insert Errors for Price Scenario 20
INSERT INTO dbo.LoanPASS_Price_Scenario_Errors (
    LoanPASS_Price_Scenario_Id,
    Source_Type__c,
    Source_Rule_Id__c,
    Error_Type__c,
    Error_Field_Id__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @PriceScenarioId,
    'rule',
    '84351',
    'blank-field',
    'field@decision-credit-score',
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);
PRINT 'Inserted Errors for Price Scenario 20.';

-- Scenario 21: id: 73a9b48f0602d81e71ed6919b4de6e0c
INSERT INTO dbo.LoanPASS_Price_Scenarios (
    LoanPASS_Product_Offering_Id,
    Adjusted_Rate__c,
    Adjusted_Price__c,
    Adjusted_Rate_Lock_Count__c,
    Adjusted_Rate_Lock_Unit__c,
    Undiscounted_Rate__c,
    Starting_Adjusted_Rate__c,
    Starting_Adjusted_Price__c,
    Status__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @ProductOfferingId,
    9.000,
    NULL,
    30,
    'days',
    NULL,
    NULL,
    NULL,
    'error',
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);
SET @PriceScenarioId = SCOPE_IDENTITY();
PRINT 'Inserted Price Scenario with Id: ' + CAST(@PriceScenarioId AS NVARCHAR(10));

-- Insert Calculated Fields for Price Scenario 21
INSERT INTO dbo.LoanPASS_Price_Scenario_Calculated_Fields (
    LoanPASS_Price_Scenario_Id,
    Field_Id__c,
    Value_Type__c,
    Enum_Type_Id__c,
    Variant_Id__c,
    Number_Value__c,
    String_Value__c,
    Duration_Count__c,
    Duration_Unit__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES
    (@PriceScenarioId, 'calc@final-interest-rate', 'number', NULL, NULL, 9.00, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@adjusted-rate-lock-period', 'duration', NULL, NULL, NULL, NULL, 30, 'days', NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@mtg-payment', 'number', NULL, NULL, 3620.81, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc-field@sgcp-investor-connect-refinance-matrix-output', 'null', NULL, NULL, NULL, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc-field@sgcp-investor-connect-purchase-matrix-output', 'null', NULL, NULL, NULL, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0);
PRINT 'Inserted Calculated Fields for Price Scenario 21.';

-- Insert Errors for Price Scenario 21
INSERT INTO dbo.LoanPASS_Price_Scenario_Errors (
    LoanPASS_Price_Scenario_Id,
    Source_Type__c,
    Source_Rule_Id__c,
    Error_Type__c,
    Error_Field_Id__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @PriceScenarioId,
    'rule',
    '84351',
    'blank-field',
    'field@decision-credit-score',
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);
PRINT 'Inserted Errors for Price Scenario 21.';


-- Scenario 22: id: 56383fb009c805719d8edd0dcb353ed1
INSERT INTO dbo.LoanPASS_Price_Scenarios (
    LoanPASS_Product_Offering_Id,
    Adjusted_Rate__c,
    Adjusted_Price__c,
    Adjusted_Rate_Lock_Count__c,
    Adjusted_Rate_Lock_Unit__c,
    Undiscounted_Rate__c,
    Starting_Adjusted_Rate__c,
    Starting_Adjusted_Price__c,
    Status__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @ProductOfferingId,
    8.875, -- Assuming this is the next rate based on the pattern
    NULL,
    30,
    'days',
    NULL,
    NULL,
    NULL,
    'error',
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);
SET @PriceScenarioId = SCOPE_IDENTITY();
PRINT 'Inserted Price Scenario with Id: ' + CAST(@PriceScenarioId AS NVARCHAR(10));

-- Insert Calculated Fields for Price Scenario 22
INSERT INTO dbo.LoanPASS_Price_Scenario_Calculated_Fields (
    LoanPASS_Price_Scenario_Id,
    Field_Id__c,
    Value_Type__c,
    Enum_Type_Id__c,
    Variant_Id__c,
    Number_Value__c,
    String_Value__c,
    Duration_Count__c,
    Duration_Unit__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES
    (@PriceScenarioId, 'calc@mtg-payment', 'number', NULL, NULL, 3580.41, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@adjusted-rate-lock-period', 'duration', NULL, NULL, NULL, NULL, 30, 'days', NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc-field@sgcp-investor-connect-refinance-matrix-output', 'null', NULL, NULL, NULL, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc-field@sgcp-investor-connect-purchase-matrix-output', 'null', NULL, NULL, NULL, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0),
    (@PriceScenarioId, 'calc@final-interest-rate', 'number', NULL, NULL, 8.875, NULL, NULL, NULL, NULL, GETUTCDATE(), GETUTCDATE(), 0);
PRINT 'Inserted Calculated Fields for Price Scenario 22.';

-- Insert Errors for Price Scenario 22
INSERT INTO dbo.LoanPASS_Price_Scenario_Errors (
    LoanPASS_Price_Scenario_Id,
    Source_Type__c,
    Source_Rule_Id__c,
    Error_Type__c,
    Error_Field_Id__c,
    Name,
    CreatedDate,
    LastModifiedDate,
    IsDeleted
)
VALUES (
    @PriceScenarioId,
    'rule',
    '84351',
    'blank-field',
    'field@decision-credit-score',
    NULL,
    GETUTCDATE(),
    GETUTCDATE(),
    0
);
PRINT 'Inserted Errors for Price Scenario 22.';

-- Commit the transaction
COMMIT TRANSACTION;
PRINT 'All data inserted successfully.';