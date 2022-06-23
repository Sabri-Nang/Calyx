CREATE TABLE IF NOT EXISTS public.cines
(
    id integer NOT NULL,
    provincia character varying(255),
    cant_pantallas integer,
    cant_butacas integer,
    cant_espacios_incaa integer,
    create_at timestamp without time zone,
    PRIMARY KEY (id)
)