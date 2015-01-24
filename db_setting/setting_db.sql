CREATE DATABASE IF NOT EXISTS curie;
USE curie;

CREATE TABLE IF NOT EXISTS song_info (
     id     int(6)     not null     auto_increment,
     title     varchar(500)     not null,
     artist    varchar(500)      default null,
     album     varchar(20)     default null, 
     image_url     varchar(300)     default null,
     lyrics     varchar(10000)     default null,
     PRIMARY KEY(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS app_info (
     id     int(6)     not null     auto_increment,
     name     varchar(20)     not null,
     googleplay_url    varchar(1000)      default null,
     android_prefix     varchar(1000)     default null,
     android_appendix     varchar(1000)     default null,
     iTunes_url     varchar(1000)     default null, 
     ios_prefix   varchar(1000)     default null,
     ios_appendix   varchar(1000)     default null,
     PRIMARY KEY(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS link_ids (
     id     int(6)     not null     auto_increment,
     song_id     int(6)     not null,
     app_id     int(6)     not null,
     link_id     varchar(300)     not null,
     PRIMARY KEY(id),
     CONSTRAINT `fk_link_app`
          FOREIGN KEY(song_id) REFERENCES song_info (id)
          ON DELETE CASCADE
          ON UPDATE RESTRICT,
     CONSTRAINT `fk_link_song`
          FOREIGN KEY(app_id) REFERENCES app_info (id)
          ON DELETE CASCADE
          ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SHOW tables;

LOAD DATA INFILE '/home/hunjaege/data/app_info' 
INTO TABLE app_info
CHARACTER SET utf8
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(@col1, @col2, @col3, @col4, @col5, @col6, @col7)
set name=@col1,  googleplay_url = @col2, android_prefix = @col3, android_appendix = @col4, iTunes_url = @col5, ios_prefix = @col6, ios_appendix = @col7;

select * from app_info;

LOAD DATA INFILE '/home/hunjaege/data/sample_2000' 
INTO TABLE song_info
CHARACTER SET utf8
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
(@col1, @col2, @col3)
set artist=@col1, title=@col2, image_url=@col3;

select * from song_info;

LOAD DATA INFILE '/home/hunjaege/data/sample_2000' 
INTO TABLE link_ids
CHARACTER SET utf8
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
(@col1, @col2, @col3, @col4)
set app_id=1, link_id = @col4, song_id=(select ifnull((select id
from song_info where title=@col2 and artist=@col1 LIMIT 1), (select id from song_info LIMIT 1)));

