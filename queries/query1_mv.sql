SELECT
    sale_date,
    category_name,
    sum(revenue) AS revenue
FROM mv_daily_category_revenue
WHERE sale_date >= today() - 30
GROUP BY sale_date, category_name