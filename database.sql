--
-- PostgreSQL database dump
--

--
-- Name: articles; Type: TABLE; Schema: public; Owner: runda_news
--

CREATE TABLE public.articles (
    id BIGSERIAL NOT NULL PRIMARY KEY,
    spider_name TEXT,
    url TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    published TIMESTAMP WITH TIME ZONE,
    categories TEXT,
    subtitle TEXT,
    author TEXT,
    photo_urls TEXT
);
