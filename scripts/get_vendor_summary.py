import sqlite3
import pandas as pd
import logging
from ingestion_db import ingest_db
from sqlalchemy import create_engine

logging.basicConfig(
    filename ="logs/get_vendor_summary.log",
    level = logging.DEBUG,
    format = "%(asctime)s - %(levelname)s - %(message)s",
    filemode = "a"
)

# Joining Tables
def create_vendor_summary(engine):
        ''' This function will merge the different tables to get the overall vendor summary and ading new columns and the resultant data '''
        vendor_sales_summary = pd.read_sql_query(""" 
        WITH FreightSummary as (
        SELECT 
                VendorNumber,
                SUM(Freight) as FreightCost
        FROM vendor_invoice
        GROUP BY VendorNumber
        ),
        
        PurchaseSummary as (
        SELECT
                p.VendorNumber,
                p.VendorName,
                p.Brand,
                p.Description,
                p.PurchasePrice,
                pp.Price as ActualPrice,
                pp.Volume,
                SUM(p.Quantity) as TotalPurchaseQuantity,
                SUM(p.Dollars) as TotalPurchaseDollars
        FROM purchases p
                JOIN purchase_prices pp 
                ON p.Brand = pp.Brand
        WHERE p.PurchasePrice > 0
        GROUP BY p.VendorNumber, p.VendorName, p.Brand, p.Description, p.PurchasePrice,pp.Price ,pp.Volume 
        ),
        
        SalesSummary as (
        SELECT
                VendorNo,
                Brand,
                SUM(SalesDollars) as TotalSalesDollars,
                SUM(SalesPrice) as TotalSalesPrice,
                SUM(SalesQuantity) as TotalSalesQuantity,
                SUM(ExciseTax) as TotalExciseTax
        FROM sales 
        GROUP BY VendorNo, Brand
        )
        
        SELECT
                ps.VendorNumber,
                ps.VendorName,
                ps.Brand,
                ps.Description,
                ps.PurchasePrice,
                ps.ActualPrice,
                ps.Volume,
                ps.TotalPurchaseQuantity,
                ps.TotalPurchaseDollars,
                ss.TotalSalesQuantity,
                ss.TotalSalesDollars,
                ss.TotalSalesPrice,
                ss.TotalExciseTax,
                fs.FreightCost
        FROM PurchaseSummary ps
        LEFT JOIN SalesSummary ss
                ON ps.VendorNumber = ss.VendorNo
                AND ps.Brand = ss.Brand
        LEFT JOIN FreightSummary fs 
                ON ps.VendorNumber = fs.VendorNumber
        ORDER BY ps.TotalPurchaseDollars DESC""", engine)            


        return vendor_sales_summary


# Data Cleaning
def clean_data(df):
    df['Volume'] = df['Volume'].astype('float64')
    df.fillna(0, inplace=True)
    df['VendorName'] = df['VendorName'].str.strip()

    df['GrossProfit'] = df['TotalSalesDollars'] - df['TotalPurchaseDollars']
    df['ProfitMargin'] = (df['GrossProfit'] / df['TotalSalesDollars']) * 100
    df['StockTurnover'] = df['TotalSalesQuantity'] / df['TotalPurchaseQuantity']
    df['SalestoPurchaseRatio'] = df['TotalSalesDollars'] / df['TotalPurchaseDollars']

    return df


if __name__ == '__main__':
    from sqlalchemy import create_engine

    engine = create_engine('sqlite:///inventory.db', connect_args={'timeout': 30})

    logging.info('Creating Vendor Summary Table.....')
    summary_df = create_vendor_summary(engine)
    logging.info(summary_df.head())

    logging.info('Clean Data.....')
    clean_df = clean_data(summary_df)
    logging.info(clean_df.head())

    logging.info('Ingesting Data.....')
    ingest_db(clean_df, 'vendor_sales_summary', engine)
    logging.info('Completed')