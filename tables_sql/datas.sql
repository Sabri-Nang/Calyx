CREATE TABLE IF NOT EXISTS public.datas
(
    id integer NOT NULL,
    cod_localidad integer,
    id_provincia integer,
    id_departamento integer,
    categoria character varying(255),
    provincia character varying(255),
    localidad character varying(255),
    nombre character varying(255),
    domicilio character varying(255),
    codigo_postal character varying(255),
    numero_telefono character varying(255),
    mail character varying(255),
    web character varying(255),
    create_at timestamp without time zone,
    PRIMARY KEY (id)
)