-- load user-defined functions
REGISTER s3n://uw-cse-344-oregon.aws.amazon.com/myudfs.jar

-- load the first chunk file into Pig
raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/btc-2010-chunk-000' USING TextLoader AS (line:chararray);

-- parse each line into ntriples
ntriples = FOREACH raw GENERATE FLATTEN(myudfs.RDFSplit3(line)) as (subject:chararray,predicate:chararray,object:chararray);
DESCRIBE ntriples;

--group the n-triples by object column
objects = GROUP ntriples BY (object) PARALLEL 50;
DESCRIBE objects;

-- flatten the objects out (because group by produces a tuple of each object
-- in the first column, and we want each object ot be a string, not a tuple),
-- and count the number of tuples associated with each object
count_by_object = FOREACH objects GENERATE FLATTEN($0), COUNT($1) as count PARALLEL 50;
DESCRIBE count_by_object;

--order the resulting tuples by their count in descending order
count_by_object_ordered = ORDER count_by_object BY (count)  PARALLEL 50;

-- show sample of the final result
DESCRIBE count_by_object_ordered;

-- count and print number of occurrences
-- all_records = GROUP count_by_object_ordered ALL;
-- record_count = FOREACH all_records GENERATE COUNT(count_by_object_ordered);
-- DUMP record_count;

-- store results into HDFS 
fs -mkdir /user/hadoop;
STORE count_by_object_ordered INTO '/user/hadoop/problem1-results USING PigStoreage();


