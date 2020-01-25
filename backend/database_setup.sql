create table admins
(
    id            int
        primary key,
    admin_id      text not null,
    password      text not null,
    add_code      text,
    access_expire text,
    added_by      text
);

create unique index admins_admin_id_uindex
    on admins (admin_id);

create table sessions
(
    token    text,
    admin_id text,
    expire   text
);

create unique index sessions_admin_id_uindex
    on sessions (admin_id);

create unique index sessions_token_uindex
    on sessions (token);



-- Adds the master admin to the database if it does not exist
insert into admins(admin_id, password, add_code)
select 'master', 'master', '12345678'
where not exists(select 1 from admins where admin_id = 'master')

-- TODO: Make database setup more robust, check tables and columns
-- currently only sets up the db from scratch and fails if it already exists