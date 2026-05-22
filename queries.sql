-- 1. Revenue per store
SELECT store_id, SUM(total_amount) AS revenue
FROM Orders
GROUP BY store_id;

-- 2. Top 10 customers
SELECT customer_id, SUM(total_amount) AS total_spent
FROM Orders
GROUP BY customer_id
ORDER BY total_spent DESC
LIMIT 10;

-- 3. Most popular item
SELECT item_id, SUM(quantity) AS total_sold
FROM Order_Items
GROUP BY item_id
ORDER BY total_sold DESC
LIMIT 1;

-- 4. Average order value
SELECT AVG(total_amount) FROM Orders;

-- 5. Busiest hour
SELECT EXTRACT(HOUR FROM order_timestamp) AS hour, COUNT(*)
FROM Orders
GROUP BY hour
ORDER BY COUNT(*) DESC;

-- 6. Top selling menu items
SELECT 
    mi.name AS item_name,
    SUM(oi.quantity) AS total_sold
FROM Order_Items oi
JOIN Menu_Items mi
    ON oi.item_id = mi.item_id
GROUP BY mi.name
ORDER BY total_sold DESC
LIMIT 10;

-- 7. Number of orders per store
SELECT 
    s.store_id,
    s.city,
    COUNT(o.order_id) AS total_orders
FROM Stores s
JOIN Orders o
    ON s.store_id = o.store_id
GROUP BY s.store_id, s.city
ORDER BY total_orders DESC;

-- 8. Customers with more than 5 orders
SELECT 
    c.customer_id,
    c.first_name,
    c.last_name,
    COUNT(o.order_id) AS order_count
FROM Customers c
JOIN Orders o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
HAVING COUNT(o.order_id) > 5
ORDER BY order_count DESC;

-- 9. Daily revenue trend
SELECT 
    DATE(order_timestamp) AS order_date,
    SUM(total_amount) AS daily_revenue
FROM Orders
GROUP BY DATE(order_timestamp)
ORDER BY order_date;

-- 10. Highest revenue generating store
SELECT 
    s.store_id,
    s.city,
    SUM(o.total_amount) AS total_revenue
FROM Stores s
JOIN Orders o
    ON s.store_id = o.store_id
GROUP BY s.store_id, s.city
ORDER BY total_revenue DESC
LIMIT 1;