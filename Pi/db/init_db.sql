--Uncomment when you actually want to nuke the DB
--DROP DATABASE IF EXISTS sensordb;
CREATE DATABASE sensordb;
USE sensordb;
CREATE TABLE time_on_pc (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp_column TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    distance FLOAT
);

CREATE TABLE aggregate_table (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp_column DATE DEFAULT CURRENT_DATE - INTERVAL 1 DAY,
    percent_time_on_pc FLOAT
);
