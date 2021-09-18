SET sql_safe_updates = FALSE;

USE defaultdb;
DROP DATABASE IF EXISTS htn CASCADE;
CREATE DATABASE IF NOT EXISTS htn;

USE htn;

CREATE TABLE accounts (
    id UUID PRIMARY KEY,
    balance INT8,
    name TEXT,
    age INT8,
    address TEXT,
    emergency_contact TEXT,
    allergies TEXT,
    blood_type TEXT,
    conditions TEXT,
    medications TEXT,
    bmi INT8,
    height INT8,
    weight INT8
);