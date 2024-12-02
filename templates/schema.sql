-- Creación de la base de datos
CREATE DATABASE sistema_asistencia;

-- Uso de la base de datos
USE sistema_asistencia;

-- Tabla de Empleados
CREATE TABLE empleados (
    codigo_empleado VARCHAR(20) PRIMARY KEY,  -- Código único para cada empleado
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    dni VARCHAR(15) NOT NULL UNIQUE,
    fecha_ingreso DATE,
    cargo VARCHAR(100),
    estado ENUM('activo', 'inactivo') DEFAULT 'activo'  -- Estado del empleado
);

-- Tabla de Asistencias
CREATE TABLE asistencias (
    codigo_asistencia VARCHAR(20) PRIMARY KEY,  -- Código único para cada registro de asistencia
    codigo_empleado VARCHAR(20),
    fecha DATE NOT NULL,
    hora_entrada TIME NOT NULL,
    hora_salida TIME,
    estado ENUM('asistió', 'no asistió', 'tarde') DEFAULT 'asistió',  -- Estado de la asistencia
    FOREIGN KEY (codigo_empleado) REFERENCES empleados(codigo_empleado) ON DELETE CASCADE
);

-- Tabla de Reportes
CREATE TABLE reportes (
    codigo_reporte VARCHAR(20) PRIMARY KEY,  -- Código único para cada reporte
    codigo_empleado VARCHAR(20),
    fecha_inicio DATE,
    fecha_fin DATE,
    total_asistencias INT DEFAULT 0,
    total_tardanzas INT DEFAULT 0,
    total_ausencias INT DEFAULT 0,
    FOREIGN KEY (codigo_empleado) REFERENCES empleados(codigo_empleado) ON DELETE CASCADE
);
