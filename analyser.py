#!/usr/bin/python3
import psycopg2


def get_queries():
    queries = [
        {
            "id": "most-popular-three-articles-ever",
            "title": "The most popular three articles of all time",
            "sql_query": """
                select a.title as article, count(l.slug) as views
                from articles a, log_cleaned l
                where a.slug = l.slug
                group by 1
                order by 2 desc
                limit 3;""",
            "answer_column": "views"
        },
        {
            "id": "most-popular-authors-ever",
            "title": "The most popular article authors of all time",
            "sql_query": """
                select au.name as author, count(l.slug) as views
                from log_cleaned l, articles ar, authors au
                where l.slug = ar.slug and ar.author = au.id
                group by 1
                order by 2 desc
                limit 10;""",
            "answer_column": "views"
        },
        {
            "id": "days-with-more-than-1-percent-request-errors",
            "title": "The days that had more than 1% of " +
                     "requests leading to errors",
            "sql_query": """
                select req.day::date, round(cast((cast(err.error_requests as
                    float)/ cast(req.requests as float))*100 as numeric), 2) as
                    errors
                from (select date_trunc('day', time) as day, count(status)
                    requests from log group by 1) as req,
                    (select date_trunc('day', time) as day, count(status)
                    error_requests from log where status not like '%200%' group
                    by 1) as err
                where req.day = err.day and (cast(err.error_requests as float)/
                    cast(req.requests as float))*100 > 1 order by 2;""",
            "answer_column": "% errors"
        }
    ]
    return queries


def write_text_block(headline, body):
    f = open("./report.txt", "a")
    f.write("##%s\n" % headline)
    for line in body:
        f.write("%s\n" % line)
    f.write("\n\n")
    f.close()


def connect_to_db():
    db = psycopg2.connect("dbname=news")
    execute_queries(db)
    db.close()


def execute_queries(db):
    queries = get_queries()
    c = db.cursor()
    for query in queries:
        c.execute(query.get("sql_query"))
        results = c.fetchall()
        stringified_rows = ["%s - %s %s" % (row[0], row[1],
                            query.get("answer_column")) for row in results]
        write_text_block(query.get("title"), stringified_rows)


connect_to_db()
