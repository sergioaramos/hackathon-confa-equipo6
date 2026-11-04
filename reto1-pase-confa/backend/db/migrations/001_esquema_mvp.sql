-- 001 · Esquema MVP de Pase CONFA (design.md, sección Datos).
-- Sin columnas de imagen, plantilla biométrica, confianza del reconocimiento ni salud (Req 13.1, 13.2).
-- Las horas se guardan con zona horaria (timestamptz); Colombia es UTC-5.
-- Tablas Deseables (eventos_borrador, solicitudes_sede) llegan en migraciones posteriores.

CREATE TABLE sedes (
    id      uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre  text NOT NULL CHECK (char_length(nombre) BETWEEN 1 AND 80),
    aforo   integer NOT NULL CHECK (aforo > 0)
);

CREATE TABLE personas (
    tipo_doc               text NOT NULL CHECK (tipo_doc ~ '^[A-Z]{1,2}$'),
    numero_doc             text NOT NULL CHECK (numero_doc ~ '^[0-9]{5,12}$'),
    nombre                 text NOT NULL CHECK (char_length(nombre) BETWEEN 1 AND 80),
    telefono               text,
    correo                 text,
    es_menor               boolean NOT NULL DEFAULT false,
    origen                 text NOT NULL CHECK (origen IN ('confa', 'sitio')),
    acepto_tratamiento_en  timestamptz,
    version_aviso          text,
    capturado_por          text,
    creado_en              timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (tipo_doc, numero_doc),
    -- Teléfono y correo solo de quien se registra en sitio; no se copian de CONFA (13.1).
    CONSTRAINT contacto_solo_registro_en_sitio
        CHECK (origen = 'sitio' OR (telefono IS NULL AND correo IS NULL)),
    -- El registro en sitio exige la aceptación del tratamiento de datos (6.3).
    CONSTRAINT registro_en_sitio_con_aceptacion
        CHECK (origen = 'confa' OR (acepto_tratamiento_en IS NOT NULL
                                    AND version_aviso IS NOT NULL
                                    AND capturado_por IS NOT NULL))
);

CREATE TABLE eventos (
    id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre              text NOT NULL CHECK (char_length(nombre) BETWEEN 1 AND 120),
    fecha               date NOT NULL,
    hora                time NOT NULL,
    sede_id             uuid NOT NULL REFERENCES sedes (id),
    tipo                text NOT NULL CHECK (tipo IN ('externo', 'interno', 'individual')),
    modalidad           text NOT NULL DEFAULT 'presencial'
                        CHECK (modalidad IN ('presencial', 'virtual', 'hibrido')),
    enlace_reunion      text,
    inscripcion_previa  boolean NOT NULL DEFAULT true,
    dirigido_a_menores  boolean NOT NULL DEFAULT false,
    cupo                integer NOT NULL CHECK (cupo > 0),
    estado              text NOT NULL DEFAULT 'abierto' CHECK (estado IN ('abierto', 'cerrado')),
    creado_por          text NOT NULL,
    origen              text NOT NULL DEFAULT 'formulario' CHECK (origen IN ('formulario', 'borrador')),
    creado_en           timestamptz NOT NULL DEFAULT now(),
    cerrado_en          timestamptz,
    CONSTRAINT cierre_coherente CHECK ((estado = 'cerrado') = (cerrado_en IS NOT NULL))
);

CREATE TABLE inscripciones (
    id                        uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    evento_id                 uuid NOT NULL REFERENCES eventos (id),
    tipo_doc                  text NOT NULL,
    numero_doc                text NOT NULL,
    nombre_cargado            text CHECK (char_length(nombre_cargado) <= 80),
    empresa                   text CHECK (char_length(empresa) <= 80),
    correo                    text,
    estado                    text NOT NULL DEFAULT 'inscrita' CHECK (estado IN ('inscrita', 'no_inscrita')),
    qr_token_hash             text UNIQUE,
    qr_version                integer NOT NULL DEFAULT 1 CHECK (qr_version > 0),
    consentimiento_grupal_en  timestamptz,
    creado_en                 timestamptz NOT NULL DEFAULT now(),
    FOREIGN KEY (tipo_doc, numero_doc) REFERENCES personas (tipo_doc, numero_doc),
    UNIQUE (evento_id, tipo_doc, numero_doc)
);

CREATE TABLE personal (
    sub     text PRIMARY KEY,
    email   text NOT NULL,
    nombre  text NOT NULL
);

-- La llave es el sub de Cognito (inmutable), nunca el correo (13.4).
CREATE TABLE personal_eventos (
    sub           text NOT NULL REFERENCES personal (sub),
    evento_id     uuid NOT NULL REFERENCES eventos (id),
    rol           text NOT NULL CHECK (rol IN ('organizador', 'logistico', 'punto_fijo')),
    asignado_por  text NOT NULL,
    asignado_en   timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (sub, evento_id, rol)
);

-- Constancia de cada intento facial, sin imagen (5.7).
CREATE TABLE consentimientos (
    id                       uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    evento_id                uuid NOT NULL REFERENCES eventos (id),
    puerta                   text NOT NULL,
    usuario                  text NOT NULL REFERENCES personal (sub),
    modo                     text NOT NULL CHECK (modo IN ('logistico', 'punto_fijo')),
    quien_acepto             text NOT NULL CHECK (quien_acepto IN ('logistico', 'titular')),
    hora                     timestamptz NOT NULL DEFAULT now(),
    version_aviso            text NOT NULL,
    mayor_de_edad_declarado  boolean NOT NULL,
    resultado                text NOT NULL CHECK (resultado IN (
                                 'RECONOCIDO', 'REPETIR', 'SIN_ROSTRO', 'VARIOS_ROSTROS',
                                 'NO_RECONOCIDO', 'FALLA_TECNICA')),
    tipo_doc                 text,
    numero_doc               text,
    -- El documento solo se guarda si la API lo reconoció.
    CONSTRAINT documento_solo_si_reconocido
        CHECK (resultado = 'RECONOCIDO' OR (tipo_doc IS NULL AND numero_doc IS NULL))
);

CREATE TABLE asistencias (
    id                    uuid PRIMARY KEY,          -- lo genera el cliente: sincronización idempotente
    evento_id             uuid NOT NULL REFERENCES eventos (id),
    tipo_doc              text NOT NULL,
    numero_doc            text NOT NULL,
    canal                 text NOT NULL DEFAULT 'presencial' CHECK (canal IN ('presencial', 'virtual')),
    metodo                text NOT NULL CHECK (metodo IN ('rostro', 'qr', 'cedula', 'grupal', 'virtual')),
    puerta                text,
    hora_servidor         timestamptz NOT NULL DEFAULT now(),
    hora_cliente          timestamptz,
    desfase_reloj_s       integer,
    tiempo_validacion_ms  integer CHECK (tiempo_validacion_ms >= 0),
    origen                text NOT NULL DEFAULT 'en_linea' CHECK (origen IN ('en_linea', 'sin_conexion')),
    consentimiento_id     uuid REFERENCES consentimientos (id),
    validado_por          text NOT NULL REFERENCES personal (sub),
    revision              boolean NOT NULL DEFAULT false,
    FOREIGN KEY (tipo_doc, numero_doc) REFERENCES personas (tipo_doc, numero_doc),
    -- Una persona cuenta una vez por canal en cada evento (1.5, 7.5, 15.6).
    UNIQUE (evento_id, tipo_doc, numero_doc, canal),
    -- Todo ingreso por rostro tiene su constancia de consentimiento (5.1, 5.7).
    CONSTRAINT rostro_con_consentimiento
        CHECK (metodo <> 'rostro' OR consentimiento_id IS NOT NULL)
);

-- Trazabilidad: quién hizo qué y cuándo (4.5, 13.5). Sin UPDATE ni DELETE para la aplicación (tarea 77).
CREATE TABLE decisiones (
    id             uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    evento_id      uuid REFERENCES eventos (id),
    tipo_doc       text,
    numero_doc     text,
    accion         text NOT NULL CHECK (accion IN (
                       'registrar', 'rechazar', 'reingreso', 'permitir_cupo', 'confirmar_evento',
                       'aprobar_sede', 'descargar_paquete', 'exportar_informe', 'descargar_qr',
                       'rotar_qr', 'asignar_rol')),
    motivo         text,
    usuario        text NOT NULL REFERENCES personal (sub),
    hora_servidor  timestamptz NOT NULL DEFAULT now(),
    hora_cliente   timestamptz
);

CREATE INDEX asistencias_por_evento ON asistencias (evento_id);
CREATE INDEX inscripciones_por_evento ON inscripciones (evento_id);
CREATE INDEX decisiones_por_evento ON decisiones (evento_id);
CREATE INDEX consentimientos_por_evento ON consentimientos (evento_id);
