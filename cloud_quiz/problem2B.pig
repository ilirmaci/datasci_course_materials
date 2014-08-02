-- load script of parsing utilities
register s3n://uw-cse-344-oregon.aws.amazon.com/myudfs.jar

-- load the test file into Pig
raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/btc-2010-chunk-000' USING TextLoader AS (line:chararray);

-- parse each line into ntriples
ntriples = FOREACH raw GENERATE FLATTEN(myudfs.RDFSplit3(line)) AS (subject:chararray,predicate:chararray,object:chararray);

-- group by subject and return the count of triples in each group
tuples_associated = FOREACH (GROUP ntriples BY subject PARALLEL 5) GENERATE group AS subject, COUNT(ntriples) AS assoc_count PARALLEL 5;

-- group again by number of associated tuples, and return count of subjects
histogram = FOREACH (GROUP tuples_associated BY assoc_count PARALLEL 5) GENERATE group AS assoc_count, COUNT(tuples_associated) AS subject_count PARALLEL 5;

-- add up number of all records
hist_count = FOREACH (GROUP histogram ALL) GENERATE COUNT(histogram);
DUMP hist_count;

fs -mkdir /home/hadoop/results;
STORE histogram INTO '/home/hadoop/results/problem2B-results USING PigStoreage();

