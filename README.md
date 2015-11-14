![Logo](fried_chili.png)

El objetivo de este proyecto es extraer la mayor cantidad de información posible de los wikis del chiliproject y transformarla en forma automática a wikis de github.

El formato de wiki usado por [Chiliproject](https://www.chiliproject.org/) es [Textile](https://en.wikipedia.org/wiki/Textile_(markup_language)).
El formato de wiki usado por Github es [Markdown](https://guides.github.com/features/mastering-markdown/)

## Analizando la base de datos del chili

Importar la base de datos:
`$ mysql -p  < database_chiliproject.sql`

```
mysql> use chiliproject;

mysql> show tables;
+-------------------------------------+
| Tables_in_chiliproject              |
+-------------------------------------+
| attachments                         |
| auth_sources                        |
| boards                              |
| changes                             |
| changesets                          |
| changesets_issues                   |
| comments                            |
| custom_fields                       |
| custom_fields_projects              |
| custom_fields_trackers              |
| custom_values                       |
| documents                           |
| enabled_modules                     |
| enumerations                        |
| groups_users                        |
| issue_categories                    |
| issue_relations                     |
| issue_statuses                      |
| issues                              |
| journal_details                     |
| journals                            |
| member_roles                        |
| members                             |
| messages                            |
| news                                |
| open_id_authentication_associations |
| open_id_authentication_nonces       |
| projects                            |
| projects_trackers                   |
| queries                             |
| repositories                        |
| roles                               |
| schema_migrations                   |
| settings                            |
| time_entries                        |
| tokens                              |
| trackers                            |
| user_preferences                    |
| users                               |
| versions                            |
| watchers                            |
| wiki_content_versions               |
| wiki_contents                       |
| wiki_pages                          |
| wiki_redirects                      |
| wikis                               |
| workflows                           |
+-------------------------------------+
47 rows in set (0.00 sec)

mysql> describe wiki_content_versions;
+-----------------+--------------+------+-----+---------+----------------+
| Field           | Type         | Null | Key | Default | Extra          |
+-----------------+--------------+------+-----+---------+----------------+
| id              | int(11)      | NO   | PRI | NULL    | auto_increment |
| wiki_content_id | int(11)      | NO   | MUL | NULL    |                |
| page_id         | int(11)      | NO   |     | NULL    |                |
| author_id       | int(11)      | YES  |     | NULL    |                |
| data            | longblob     | YES  |     | NULL    |                |
| compression     | varchar(6)   | YES  |     |         |                |
| comments        | varchar(255) | YES  |     |         |                |
| updated_on      | datetime     | NO   | MUL | NULL    |                |
| version         | int(11)      | NO   |     | NULL    |                |
+-----------------+--------------+------+-----+---------+----------------+
9 rows in set (0.00 sec)

mysql> describe wiki_contents;
+--------------+----------+------+-----+---------+----------------+
| Field        | Type     | Null | Key | Default | Extra          |
+--------------+----------+------+-----+---------+----------------+
| id           | int(11)  | NO   | PRI | NULL    | auto_increment |
| page_id      | int(11)  | NO   | MUL | NULL    |                |
| author_id    | int(11)  | YES  | MUL | NULL    |                |
| text         | longtext | YES  |     | NULL    |                |
| updated_on   | datetime | NO   |     | NULL    |                |
| lock_version | int(11)  | NO   |     | NULL    |                |
+--------------+----------+------+-----+---------+----------------+
6 rows in set (0.00 sec)

mysql> describe wiki_pages;
+------------+--------------+------+-----+---------+----------------+
| Field      | Type         | Null | Key | Default | Extra          |
+------------+--------------+------+-----+---------+----------------+
| id         | int(11)      | NO   | PRI | NULL    | auto_increment |
| wiki_id    | int(11)      | NO   | MUL | NULL    |                |
| title      | varchar(255) | NO   |     | NULL    |                |
| created_on | datetime     | NO   |     | NULL    |                |
| protected  | tinyint(1)   | NO   |     | 0       |                |
| parent_id  | int(11)      | YES  | MUL | NULL    |                |
+------------+--------------+------+-----+---------+----------------+
6 rows in set (0.01 sec)

mysql> describe wiki_redirects;
+--------------+--------------+------+-----+---------+----------------+
| Field        | Type         | Null | Key | Default | Extra          |
+--------------+--------------+------+-----+---------+----------------+
| id           | int(11)      | NO   | PRI | NULL    | auto_increment |
| wiki_id      | int(11)      | NO   | MUL | NULL    |                |
| title        | varchar(255) | YES  |     | NULL    |                |
| redirects_to | varchar(255) | YES  |     | NULL    |                |
| created_on   | datetime     | NO   |     | NULL    |                |
+--------------+--------------+------+-----+---------+----------------+
5 rows in set (0.00 sec)

mysql> describe wikis;
+------------+--------------+------+-----+---------+----------------+
| Field      | Type         | Null | Key | Default | Extra          |
+------------+--------------+------+-----+---------+----------------+
| id         | int(11)      | NO   | PRI | NULL    | auto_increment |
| project_id | int(11)      | NO   | MUL | NULL    |                |
| start_page | varchar(255) | NO   |     | NULL    |                |
| status     | int(11)      | NO   |     | 1       |                |
+------------+--------------+------+-----+---------+----------------+
4 rows in set (0.00 sec)

mysql> describe attachments;
+----------------+--------------+------+-----+---------+----------------+
| Field          | Type         | Null | Key | Default | Extra          |
+----------------+--------------+------+-----+---------+----------------+
| id             | int(11)      | NO   | PRI | NULL    | auto_increment |
| container_id   | int(11)      | NO   | MUL | 0       |                |
| container_type | varchar(30)  | NO   |     |         |                |
| filename       | varchar(255) | NO   |     |         |                |
| disk_filename  | varchar(255) | NO   |     |         |                |
| filesize       | int(11)      | NO   |     | 0       |                |
| content_type   | varchar(255) | YES  |     |         |                |
| digest         | varchar(40)  | NO   |     |         |                |
| downloads      | int(11)      | NO   |     | 0       |                |
| author_id      | int(11)      | NO   | MUL | 0       |                |
| created_on     | datetime     | YES  | MUL | NULL    |                |
| description    | varchar(255) | YES  |     | NULL    |                |
+----------------+--------------+------+-----+---------+----------------+
12 rows in set (0.00 sec)

mysql> describe documents;
+-------------+-------------+------+-----+---------+----------------+
| Field       | Type        | Null | Key | Default | Extra          |
+-------------+-------------+------+-----+---------+----------------+
| id          | int(11)     | NO   | PRI | NULL    | auto_increment |
| project_id  | int(11)     | NO   | MUL | 0       |                |
| category_id | int(11)     | NO   | MUL | 0       |                |
| title       | varchar(60) | NO   |     |         |                |
| description | text        | YES  |     | NULL    |                |
| created_on  | datetime    | YES  | MUL | NULL    |                |
+-------------+-------------+------+-----+---------+----------------+
6 rows in set (0.00 sec)

mysql> describe projects;
+-------------+--------------+------+-----+---------+----------------+
| Field       | Type         | Null | Key | Default | Extra          |
+-------------+--------------+------+-----+---------+----------------+
| id          | int(11)      | NO   | PRI | NULL    | auto_increment |
| name        | varchar(255) | NO   |     |         |                |
| description | text         | YES  |     | NULL    |                |
| homepage    | varchar(255) | YES  |     |         |                |
| is_public   | tinyint(1)   | NO   |     | 1       |                |
| parent_id   | int(11)      | YES  |     | NULL    |                |
| created_on  | datetime     | YES  |     | NULL    |                |
| updated_on  | datetime     | YES  |     | NULL    |                |
| identifier  | varchar(255) | YES  |     | NULL    |                |
| status      | int(11)      | NO   |     | 1       |                |
| lft         | int(11)      | YES  | MUL | NULL    |                |
| rgt         | int(11)      | YES  | MUL | NULL    |                |
+-------------+--------------+------+-----+---------+----------------+
12 rows in set (0.00 sec)
```

## Paquetes para conectarse a la base de datos usando Python

`$ sudo apt-get install python-sqlalchemy`
`$ sudo apt-get install python-mysqldb`


## Herramienta para convertir el wiki Textile a Markdown:

http://pandoc.org/
https://github.com/jgm/pandoc



