SELECT COUNT(*) 
FROM (
    SELECT docid
    FROM Frequency
    GROUP BY docid
    HAVING sum(count) > 300
) x; 

