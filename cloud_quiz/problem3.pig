-- load script of parsing utilities
register s3n://uw-cse-344-oregon.aws.amazon.com/myudfs.jar

-- load the test file into Pig
raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/btc-2010-chunk-000' USING TextLoader AS (line:chararray);

-- parse each line into ntriples
ntriples_all = FOREACH raw GENERATE FLATTEN(myudfs.RDFSplit3(line)) AS (subject:chararray,predicate:chararray,object:chararray);

-- only keep data with "rdfabout.com" in it
ntriples = FILTER ntriples_all BY subject MATCHES '.*rdfabout\\.com.*';

-- make second copy of ntriples
ntriples2 = FOREACH ntriples GENERATE subject AS subject2, predicate as predicate2, object AS object2;

-- join the two aliases to find all chains of length 2
joined = JOIN ntriples BY object, ntriples2 BY subject2;
joined_distinct = DISTINCT joined;

-- count all rows
row_count = FOREACH (GROUP joined_distinct ALL) GENERATE COUNT(joined_distinct);
DUMP row_count;


