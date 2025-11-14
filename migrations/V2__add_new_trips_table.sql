create table trips (
    id serial primary key,
    title text not null,
    start_date timestamp not null,
    end_date timestamp not null
)