create table admins
(
    id          int primary key,
    admin_id    text not null,
    password    text not null,
    add_code    text,
    last_access text,
    added_by    text
);

create unique index admins_admin_id_uindex
    on admins (admin_id);

-- Adds the master admin to the database if it does not exist
insert into admins(admin_id, password, add_code)
select 'master', 'master', '12345678'
where not exists(select 1 from admins where admin_id = 'master')

-- TODO: Make database setup more robust, check tables and columns
-- currently only sets up the db from scratch and fails if it already exists