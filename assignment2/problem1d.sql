SELECT COUNT(*) 
FROM (
    SELECT docid 
    FROM Frequency
    WHERE term = "parliament"
) x; 
