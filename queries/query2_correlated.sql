WITH revenue_by_region_category AS (
    SELECT
        region_name,
        category_name,
        sum(total) AS revenue
    FROM sales
    WHERE sale_date >= today() - 30
    GROUP BY region_name, category_name
),
ranked AS (
    SELECT
        region_name,
        category_name,
        revenue,
        (
            SELECT count() + 1
            FROM revenue_by_region_category r2
            WHERE r2.region_name = r1.region_name
              AND r2.revenue > r1.revenue
        ) AS rank
    FROM revenue_by_region_category r1
)
SELECT region_name, category_name, revenue, rank
FROM ranked
WHERE rank <= 3
ORDER BY region_name, rank