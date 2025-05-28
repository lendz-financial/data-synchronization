-- Drop Table Script for LoanPASS Database

-- Drop dbo.LoanPASS_Price_Scenario_Errors
-- This table depends on dbo.LoanPASS_Price_Scenarios
IF OBJECT_ID('dbo.LoanPASS_Price_Scenario_Errors', 'U') IS NOT NULL
BEGIN
    DROP TABLE dbo.LoanPASS_Price_Scenario_Errors;
    PRINT 'Table dbo.LoanPASS_Price_Scenario_Errors dropped successfully.';
END
ELSE
BEGIN
    PRINT 'Table dbo.LoanPASS_Price_Scenario_Errors does not exist.';
END;

-- Drop dbo.LoanPASS_Price_Scenario_Calculated_Fields
-- This table depends on dbo.LoanPASS_Price_Scenarios
IF OBJECT_ID('dbo.LoanPASS_Price_Scenario_Calculated_Fields', 'U') IS NOT NULL
BEGIN
    DROP TABLE dbo.LoanPASS_Price_Scenario_Calculated_Fields;
    PRINT 'Table dbo.LoanPASS_Price_Scenario_Calculated_Fields dropped successfully.';
END
ELSE
BEGIN
    PRINT 'Table dbo.LoanPASS_Price_Scenario_Calculated_Fields does not exist.';
END;

-- Drop dbo.LoanPASS_Price_Scenarios
-- This table depends on dbo.LoanPASS_Product_Offerings
IF OBJECT_ID('dbo.LoanPASS_Price_Scenarios', 'U') IS NOT NULL
BEGIN
    DROP TABLE dbo.LoanPASS_Price_Scenarios;
    PRINT 'Table dbo.LoanPASS_Price_Scenarios dropped successfully.';
END
ELSE
BEGIN
    PRINT 'Table dbo.LoanPASS_Price_Scenarios does not exist.';
END;

-- Drop dbo.LoanPASS_Product_Calculated_Fields
-- This table depends on dbo.LoanPASS_Product_Offerings
IF OBJECT_ID('dbo.LoanPASS_Product_Calculated_Fields', 'U') IS NOT NULL
BEGIN
    DROP TABLE dbo.LoanPASS_Product_Calculated_Fields;
    PRINT 'Table dbo.LoanPASS_Product_Calculated_Fields dropped successfully.';
END
ELSE
BEGIN
    PRINT 'Table dbo.LoanPASS_Product_Calculated_Fields does not exist.';
END;

-- Drop dbo.LoanPASS_Product_Offerings
-- This is the parent table and should be dropped last
IF OBJECT_ID('dbo.LoanPASS_Product_Offerings', 'U') IS NOT NULL
BEGIN
    DROP TABLE dbo.LoanPASS_Product_Offerings;
    PRINT 'Table dbo.LoanPASS_Product_Offerings dropped successfully.';
END
ELSE
BEGIN
    PRINT 'Table dbo.LoanPASS_Product_Offerings does not exist.';
END;