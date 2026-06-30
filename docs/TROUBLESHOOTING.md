# Guía de diagnóstico rápido

Esta guía ayuda a interpretar dos fallos frecuentes al operar el orquestador desde Git Bash o una terminal Windows: rutas de red incompletas y Docker no disponible.

## `tracert -d 10.1.2.3` termina en `Host de destino inaccesible`

Ejemplo observado:

```text
5    47 ms    18 ms    24 ms  10.0.2.1
6     *     10.0.2.1  informes: Host de destino inaccesible.
```

Esto indica que el salto `10.0.2.1` sí responde, pero no tiene una ruta válida hacia `10.1.2.3` o está bloqueando el tráfico hacia ese destino. No es un problema de DNS porque el comando usa `-d` y no intenta resolver nombres.

Checklist recomendado:

1. Confirmar que el host destino existe y está encendido:
   ```powershell
   ping 10.1.2.3
   ```
2. Validar la ruta local en Windows:
   ```powershell
   route print
   ```
3. Revisar la tabla de rutas del gateway `10.0.2.1` y confirmar que conoce la red `10.1.2.0/24` o la subred real donde vive `10.1.2.3`.
4. Verificar firewall o ACL entre `10.0.2.1` y `10.1.2.3`.
5. Si `10.1.2.3` pertenece a una VPN, levantar la VPN antes de ejecutar el orquestador.

## `bash: docker: command not found`

El mensaje significa que la terminal no encuentra el binario `docker` en el `PATH`. En Git Bash para Windows suele pasar por una de estas causas:

- Docker Desktop no está instalado.
- Docker Desktop está instalado, pero no está iniciado.
- La ruta de Docker no fue agregada al `PATH` disponible para Git Bash.

Checklist recomendado:

1. Instalar Docker Desktop para Windows si todavía no existe.
2. Abrir Docker Desktop y esperar a que el motor quede en estado `Running`.
3. Cerrar y reabrir Git Bash.
4. Validar que Docker esté disponible:
   ```bash
   docker --version
   docker info
   ```
5. Si Git Bash aún no encuentra Docker, revisar que esta ruta exista en el `PATH` de Windows:
   ```text
   C:\Program Files\Docker\Docker\resources\bin
   ```

## Levantar Oracle XE para pruebas locales

Cuando Docker ya esté disponible, usar un nombre de contenedor estable y definir una contraseña explícita:

```bash
docker run -d \
  --name oracle-xe \
  -p 1521:1521 \
  -e ORACLE_PASSWORD=Oracle123 \
  gvenzl/oracle-xe
```

Comprobar el estado:

```bash
docker ps --filter name=oracle-xe
```

Si el puerto `1521` ya está ocupado, cambiar el puerto local, por ejemplo `-p 1522:1521`.
