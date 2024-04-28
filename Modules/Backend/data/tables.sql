CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

create table if not exists person (
    person_id serial primary key,
    name text,
    surname text,
    hidden bool default false,
    properties jsonb
);

create table if not exists device (
    device_id serial primary key,
    device_name text not null unique,
    name text,
    sensor_types smallint[],
    latitude double precision,
    longitude double precision,
    active bool default true,
    properties jsonb,
    person_id int references person(person_id)
);

create table if not exists device_log (
    time timestamptz not null,
    device_id int not null,
    sensor_type smallint default 1,
    value double precision not null
);

select create_hypertable('device_log', 'time', if_not_exists => TRUE);

create index if not exists device_time_idx on device_log (device_id, time desc);