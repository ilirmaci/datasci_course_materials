-- load script of parsing utilities
register s3n://uw-cse-344-oregon.aws.amazon.com/myudfs.jar

-- load the test file into Pig
raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/cse344-test-file' USING TextLoader AS (line:chararray);

-- parse each line into ntriples
ntriples = FOREACH raw GENERATE FLATTEN(myudfs.RDFSplit3(line)) AS (subject:chararray,predicate:chararray,object:chararray);

-- group by subject and return the count of triples in each group
tuples_associated = FOREACH (GROUP ntriples BY subject) GENERATE group AS subject, COUNT(ntriples) AS assoc_count;

-- group again by number of associated tuples, and return count of subjects
histogram = FOREACH (GROUP tuples_associated BY assoc_count) GENERATE group AS assoc_count, COUNT(tuples_associated) AS subject_count;

DUMP histogram;

fs -mkdir /user/hadoop;
STORE histogram INTO '/user/hadoop/problem2A-results USING PigStoreage();
