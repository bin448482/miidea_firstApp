show databases;
create database miidea_encryption_keys_db;
grant usage on *.* to dev@localhost identified by 'miidea299553';
grant all privileges on miidea_encryption_keys_db.* to dev@localhost;
use miidea_encryption_keys_db;
SET PASSWORD FOR 'dev@localhost' = PASSWORD('miidea299553');
