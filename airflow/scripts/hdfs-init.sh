#!/bin/bash
hdfs dfs -chmod -R 777 /user/hive/warehouse || hdfs dfs -mkdir -p /user/hive/warehouse && hdfs dfs -chmod -R 777 /user/hive/warehouse
