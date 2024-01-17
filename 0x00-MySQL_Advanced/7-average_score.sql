-- 7-average_score.sql

-- Write a SQL script that creates a stored procedure ComputeAverageScoreForUser that computes and store the average score for a student. Note: An average score can be a decimal
DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser(
    IN p_user_id INT
)
BEGIN
    DECLARE v_total_score FLOAT;
    DECLARE v_number_of_projects INT;

    SELECT SUM(score), COUNT(DISTINCT project_id)
    INTO v_total_score, v_number_of_projects
    FROM corrections
    WHERE user_id = p_user_id;

    UPDATE users
    SET average_score = IFNULL(v_total_score / NULLIF(v_number_of_projects, 0), 0)
    WHERE id = p_user_id;
END;
//

DELIMITER ;
