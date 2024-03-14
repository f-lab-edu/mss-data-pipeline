-- postgres create table sql

CREATE TABLE goods(
goods_id INTEGER PRIMARY KEY,
name VARCHAR NOT NULL,
main_thumbnail_url VARCHAR,
regular_price INTEGER NOT NULL,
sale_price INTEGER NOT NULL,
category VARCHAR,
sub_category VARCHAR,
brand VARCHAR NOT NULL,
view_in_recent_month INTEGER,
sales_in_recent_year INTEGER,
likes INTEGER,
star_rating numeric(2, 1),
reviews INTEGER,
created_at TIMESTAMP NOT NULL
);

CREATE TABLE review(
review_id INTEGER PRIMARY KEY,
goods_id INTEGER ,
content VARCHAR NOT NULL,
main_thumbnail_url VARCHAR,
likes INTEGER,
create_at TIMESTAMP NOT NULL
);

ALTER TABLE review ADD CONSTRAINT review_good_id_fk FOREIGN KEY (goods_id) REFERENCES goods(goods_id);