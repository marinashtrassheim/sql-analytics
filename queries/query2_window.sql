WITH revenue_by_region_category AS (
    SELECT
        region_name,
        category_name,
        sum(total) AS revenue
    FROM sales
    WHERE sale_date >= today() - 30
    GROUP BY region_name, category_name
)
SELECT
    region_name,
    category_name,
    revenue,
    rank() OVER (PARTITION BY region_name ORDER BY revenue DESC) AS rank
FROM revenue_by_region_category
QUALIFY rank <= 3
ORDER BY region_name, rank