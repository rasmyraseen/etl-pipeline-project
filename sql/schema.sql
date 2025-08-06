-- Cleaned & Enriched Sales Table
CREATE TABLE SalesEnriched (
    SaleID INT PRIMARY KEY,
    ProductID INT,
    SaleDate DATE,
    SaleAmount FLOAT,
    Currency VARCHAR(10),
    ProductName VARCHAR(100),
    Category VARCHAR(50),
    SaleAmountUSD FLOAT,s
    ConversionTime DATETIME
);

-- RejectedRecords 
CREATE TABLE RejectedRecords (
    SaleID INT,
    ProductID INT,
    SaleDate DATE,
    SaleAmount VARCHAR(50),
    Currency VARCHAR(10),
    ProductName VARCHAR(100),
    Category VARCHAR(50),
    SaleAmountUSD FLOAT,
    ErrorType VARCHAR(50),
    ErrorTimestamp DATETIME
);
