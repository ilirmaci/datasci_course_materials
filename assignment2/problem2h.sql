SELECT freq 
FROM (
    SELECT A.docid as docidA, B.docid as docidB, sum(A.count * B.count) AS freq
    FROM Frequency A, Frequency B
    WHERE A.term = B.term AND docidA < docidB
    GROUP BY docidA, docidB
    HAVING A.docid = "10080_txt_crude" 
        AND B.docid = "17035_txt_earn");
