-- 101-average_weighted_score.sql
-- Write a SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers that computes and store the average weighted score for all students.
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE weighted_sum FLOAT;
    DECLARE total_weight INT;

    SET weighted_sum = 0;
    SET total_weight = 0;

    DECLARE done INT DEFAULT FALSE;
    DECLARE user_id INT;
    DECLARE project_weight INT;
    DECLARE project_score FLOAT;
    
    DECLARE cur CURSOR FOR
        SELECT c.user_id, p.weight, c.score
        FROM corrections c
        JOIN projects p ON c.project_id = p.id;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO user_id, project_weight, project_score;

        IF done THEN
            LEAVE read_loop;
        END IF;

        SET weighted_sum = weighted_sum + (project_score * project_weight);
        SET total_weight = total_weight + project_weight;
    END LOOP;

    CLOSE cur;

    UPDATE users
    SET average_score = IF(total_weight > 0, weighted_sum / total_weight, 0);

END //

DELIMITER ;
