# Log Analysis
log analysis is part of Udacity's full-stack nanodegree. Its purpose is to generate insights from a database containing users logs, authors and articles data.

The database is a postgresql database containing 3 main tables (`log` - `articles` - `authors`).

The aim of this simple tool is to run certain static sql queries against the database from python code and generate a report in a text file.

Before executing python code, an extra view named `log_cleared` have to be created in the database. [check below](#creating-a-view)

## Table of Contents
* [Quick Start](#quick-start)
* [Creating a View](#creating-a-view)
* [Code Design](#code-design)

## Quick Start
* Install vagrant, VM and configuration files following [the instructions at Udacity](https://classroom.udacity.com/nanodegrees/nd004-ent/parts/72d6fe39-3e47-45b4-ac52-9300b146094f/modules/0f94ae26-c39d-4231-924b-b1eb6e06cf41/lessons/5475ecd6-cfdb-4418-85a2-f2583074c08d/concepts/14c72fe3-e3fe-4959-9c4b-467cf5b7c3a0)
* Run vagrant Virtual machine using `vagrant ssh`
* From vagrant terminal:
    * `psql news`  => to enter the database
    * create a view named `log_cleared`
        ```sql
        create view log_cleaned as (select split_part(path, '/', 3) slug, ip, method, status, time, id from log
        ```
    * `ctrl + d` => to exit the database
    * ```bash
        python3 analyser.py
        ```
        => to run the program
    * check the generated output at `report.txt`
    

## Creating a View
A view named `log_cleared` is created before running python code or fetching anything from the database.

`log_cleared` view contains the same columns as `log` table except that the `path` column is split and the part corresponding to an article slug is stored in a new column in the view named `slug`

To create the view, execute this statement inside `psql`
```sql
create view log_cleaned as (select split_part(path, '/', 3) slug, ip, method, status, time, id from log
```

# Code Design
The python code of the program is formed of 4 functions/parts:

* `get_queries` function stores and returns the static sql queries in addition to other descriptive info about the query.

* `write_text_block` function writes whatever text you feed it into `report.txt` file. So, it writes the formatted results of the queries to `report.txt`

* `connect_to_db` function connects only to the database, no more.

* `execute_queries` function sends sql queries to the database to execute it and return the results, then feed them to `write_text_block` to generate insights into `report.txt`