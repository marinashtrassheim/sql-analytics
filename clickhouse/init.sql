CREATE TABLE IF NOT EXISTS sales
(
    sale_id        UInt64,
    sale_date      Date,
    sale_datetime  DateTime,
    product_id     UInt32,
    product_name   String,
    category_id    UInt8,
    category_name  String,
    region_id      UInt8,
    region_name    String,
    customer_id    UInt32,
    customer_age   UInt8,
    customer_gender LowCardinality(String),
    quantity       UInt16,
    price          Decimal(10,2),
    discount       Float32,
    total          Decimal(12,2)
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(sale_date)
ORDER BY (sale_date, category_id, region_id)
SETTINGS index_granularity = 8192;

-- Создаём материализованное представление для агрегатов по дням и категориям
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_daily_category_revenue
ENGINE = SummingMergeTree()
PARTITION BY toYYYYMM(sale_date)
ORDER BY (sale_date, category_id)
AS
SELECT
    sale_date,
    category_id,
    category_name,
    sum(total) AS revenue,
    sum(quantity) AS total_quantity,
    count() AS orders
FROM sales
GROUP BY sale_date, category_id, category_name;