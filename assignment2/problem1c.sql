SELECT COUNT(*) 
FROM (
    SELECT DISTINCT term 
    FROM Frequency
    WHERE docid IN ("10398_txt_earn", "925_txt_trade") AND count = 1
) x; 

