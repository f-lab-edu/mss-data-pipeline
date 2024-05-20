-- postgres create table sql

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE immutable_goods_info
(
    goods_id           INTEGER PRIMARY KEY,
    name               VARCHAR   NOT NULL,
    main_thumbnail_url VARCHAR,
    regular_price      INTEGER   NOT NULL,
    category           VARCHAR,
    sub_category       VARCHAR,
    brand              VARCHAR   NOT NULL,
    created_at         TIMESTAMP NOT NULL
);

CREATE TABLE review
(
    review_id          INTEGER PRIMARY KEY,
    goods_id           INTEGER,
    content            VARCHAR   NOT NULL,
    main_thumbnail_url VARCHAR,
    likes              INTEGER,
    created_at         TIMESTAMP NOT NULL
);

CREATE TABLE mutable_goods_info
(
    mutable_goods_info_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    goods_id              INTEGER,
    sale_price            INTEGER   NOT NULL,
    views_in_recent_month INTEGER,
    sales_in_recent_year  INTEGER,
    likes                 INTEGER,
    star_rating           numeric(2, 1),
    reviews               INTEGER,
    created_at            TIMESTAMP NOT NULL
);

ALTER TABLE review ADD CONSTRAINT review_goods_id_fk FOREIGN KEY (goods_id) REFERENCES immutable_goods_info(goods_id);
ALTER TABLE mutable_goods_info ADD CONSTRAINT mutable_goods_info_goods_id_fk FOREIGN KEY (goods_id) REFERENCES immutable_goods_info(goods_id);

CREATE TABLE sales_by_price_and_category
(
    goods_id integer,
    category varchar,
    sales integer,
    price_range integer,
    PRIMARY KEY (goods_id, price_range)
);

CREATE TABLE review_word_frequency
(
    goods_id integer,
    word     varchar,
    count    integer,
    PRIMARY KEY (goods_id, word)
);