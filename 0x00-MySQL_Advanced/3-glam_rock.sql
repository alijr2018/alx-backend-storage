-- 3-glam_rock.sql
-- Write a SQL script that lists all bands with Glam rock as their main style, ranked by their longevity
SELECT
    band_name,
    IF(formed > 0, IF(split > 0, split - formed, YEAR(CURDATE()) - formed), 0) AS lifespan
FROM
    metal_bands
WHERE
    main_style = 'Glam rock'
ORDER BY
    lifespan DESC;
