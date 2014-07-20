SELECT COUNT(*) 
FROM (
    SELECT o.docid 
    FROM Frequency o
    WHERE o.term = "transactions"
        AND docid IN (
            SELECT i.docid 
            FROM Frequency i
            WHERE i.term = "world")
) x; 

