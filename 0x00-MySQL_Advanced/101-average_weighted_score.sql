-- 101-average_weighted_score.sql
-- Write a SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers that computes and store the average weighted score for all students.
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE user_id_param INT;
    
    DECLARE user_cursor CURSOR FOR SELECT id FROM users;
    
    DECLARE done INT DEFAULT FALSE;
    
    DECLARE total_score FLOAT;
    DECLARE total_weight INT;
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    OPEN user_cursor;
    
    users_loop: LOOP
        FETCH user_cursor INTO user_id_param;
        
        SELECT SUM(c.score ** p.weight), SUM(p.weight)
        INTO total_score, total_weight
                
        UPDATE users
        SET average_score = total_score / total_weight
        WHERE id = user_id_param;
    END LOOP;
    
    CLOSE user_cursor;
END //
DELIMITER ;
