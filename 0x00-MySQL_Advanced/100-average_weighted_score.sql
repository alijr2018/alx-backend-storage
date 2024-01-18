-- 100-average_weighted_score.sql

-- Write a SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser that computes and store the average weighted score for a student.
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id_param INT)
BEGIN
    DECLARE total_score FLOAT;
    DECLARE total_weight INT;
    
    SELECT SUM(c.score * p.weight), SUM(p.weight)
    INTO total_score, total_weight
    FROM corrections c
    JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = user_id_param;
    
    UPDATE users
    SET average_score = total_score / total_weight
    WHERE id = user_id_param;
END //
DELIMITER ;
