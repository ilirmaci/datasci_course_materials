# This script reads the test data from the cloud quiz
# in Coursera's Introduction to Data Science for testing and
# visualizing the data before running Hadoop/Pig scripts

library(data.table)

setwd("/data/Courses/Data science/datasci_course_materials/cloud_quiz")
d <- read.table("cse344-test-file", sep = " ", 
                header=FALSE, comment.char = "")
setDT(d)
d[, V5 := NULL]   ## last column is useless
setnames(d, c("subject", "predicate", "object", "source"))

counts <- d[, list(assoc_count=.N), by=subject]
count_of_counts <- counts[, list(cofc=.N), by=assoc_count] ## Problem 2A

d2 <- copy(d)
setkey(d, subject)
setkey(d2, subject)
nrow(d[d2, allow.cartesian=TRUE]) ## Problem 3 test
