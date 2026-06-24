SELECT
    sale_date,
    category_name,
    sum(total) AS revenue
FROM sales
WHERE sale_date >= today() - 30
GROUP BY sale_date, category_name