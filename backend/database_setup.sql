create table admins
(
    id          int
        constraint admins_pk
            primary key,
    email       text,
    admin_id    text not null,
    password    text not null,
    add_code    text,
    last_access text not null,
    added_by    text not null
);

create unique index admins_admin_id_uindex
    on admins (admin_id);

-- TODO: Make database setup more robust, check tables and columns
-- currently only sets up the db from scratch and fails if it already exists