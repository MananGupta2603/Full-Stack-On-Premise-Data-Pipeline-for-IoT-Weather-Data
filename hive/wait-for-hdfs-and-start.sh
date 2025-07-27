#!/bin/bash
echo "⏳ Waiting for HDFS (hadoop-namenode:9000)..."
until hdfs dfs -ls /; do
  echo "⏳ HDFS not ready, retrying in 5s..."
  sleep 5
done

echo "✅ HDFS is ready. Starting Hive Metastore..."
/opt/hive/bin/hive --service metastore
