CREATE TABLE IF NOT EXISTS registros
(
    id integer NOT NULL,
    tipo_registro character varying(255),
    registro character varying(255),
    cant_registros integer,
    create_at timestamp without time zone,
    PRIMARY KEY (id)
)