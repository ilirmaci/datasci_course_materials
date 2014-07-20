CREATE VIEW qfrequency AS
    SELECT * FROM frequency
    UNION
    SELECT 'q' as docid, 'washington' as term, 1 as count 
    UNION
    SELECT 'q' as docid, 'taxes' as term, 1 as count
    UNION 
    SELECT 'q' as docid, 'treasury' as term, 1 as count;


SELECT max(freq) 
FROM (
    SELECT A.docid as docidA, B.docid as docidB, sum(A.count * B.count) AS freq
    FROM qfrequency A, qfrequency B
    WHERE A.term = B.term AND docidA < docidB
    GROUP BY docidA, docidB
    HAVING B.docid = "q"
    );
