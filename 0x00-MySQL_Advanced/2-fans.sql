-- 2-fans.sql
-- Write a SQL script that ranks country origins of bands
SELECT origin, COUNT(DISTINCT fan_id) AS nb_fans
FROM metal_bands
GROUP BY origin
ORDER BY nb_fans DESC;
