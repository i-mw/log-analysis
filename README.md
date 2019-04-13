# Log Analysis
log analysis is part of Udacity's full-stack nanodegree. Its purpose is to generate insights from a database containing users logs, authors and articles data.

The database is a postgresql database containing 3 main tables (`log` - `articles` - `authors`).

The aim of this simple tool is to run certain static sql queries against the database from python code and generate a report in a text file.

Before executing python code, an extra view named `log_cleared` have to be created in the database. [check below](#creating-a-view)

## Table of Contents
* [Installation Guide](#installation-guide)
* [Creating a View](#creating-a-view)
* [Code Design](#code-design)

## Installation Guide
* Install vagrant, VM and configuration file
    * download and install virtual box version that corresponds to your operating system from [here](https://www.virtualbox.org/wiki/Downloads)
    * download and install vagrant version that corresponds to your operating system from [here](https://www.vagrantup.com/downloads.html)
    * make sure that vagrant is installed by running this command in your terminal `vagrant --version`. N.B. if you're using windows os, will need to install and use git terminal
    * download VM configuration
        * download and unzip [this file](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip) offered by Udacity
        * you'll end with a directory containing the configuration file. `cd` to that directory
        * start the virtual machine by running `vagrant up`. This will cause Vagrant to download the Linux operating system and install it.
        * clone the contents of this github repository to the directory containing the configuration file, This is the shared folder with your virtual machine.
            ```
            git clone https://github.com/i-mw/log-analysis
            ```

* Run vagrant Virtual machine:
    * `cd` to the folder containing vagrant configuration file
    * `vagrant ssh`
* From vagrant terminal:
    * `cd /vagrant/log-analysis` to move to the project directory on the shared folder
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