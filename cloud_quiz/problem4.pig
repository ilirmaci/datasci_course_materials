-- load script of parsing utilities
register s3n://uw-cse-344-oregon.aws.amazon.com/myudfs.jar

SET DEFAULT_PARALLEL 30;

-- load the test file into Pig
raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/btc-2010-chunk-*' USING TextLoader AS (line:chararray);

-- parse each line into ntriples
ntriples = FOREACH raw GENERATE FLATTEN(myudfs.RDFSplit3(line)) AS (subject:chararray,predicate:chararray,object:chararray);

-- group by subject and return the count of triples in each group
tuples_associated = FOREACH (GROUP ntriples BY subject) GENERATE group AS subject, COUNT(ntriples) AS assoc_count;

-- group again by number of associated tuples, and return count of subjects
histogram = FOREACH (GROUP tuples_associated BY assoc_count) GENERATE group AS assoc_count, COUNT(tuples_associated) AS subject_count;

-- count number of histogram tuples first by grouping it to parallelize
-- histogram_grouped = GROUP histogram BY assoc_count;
-- total_count = FOREACH (GROUP histogram_grouped ALL) GENERATE COUNT(histogram_grouped);
-- DUMP total_count;

fs -mkdir /home/hadoop/results;
STORE histogram INTO '/home/hadoop/results/problem4-results USING PigStoreage();

