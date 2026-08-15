# Cifrado con OpenSSL (Demo educativa)

Scripts en Python que cifran y descifran archivos de una carpeta usando OpenSSL (AES-256-CBC), para ejemplificar de forma didáctica cómo funciona el mecanismo de un ransomware.

> **ADVERTENCIA**: Proyecto exclusivamente educativo. Úsalo solo en entornos aislados y con archivos de prueba. No cifres datos importantes sin tener copias de seguridad.

## Requisitos

- Python 3.6+
- OpenSSL en el PATH (`openssl version`)

## Uso

Cifrar todos los archivos de una carpeta:

```
python cifrar.py C:\ruta\a\carpeta
```

Descifrar los archivos `.enc`:

```
python descifrar.py C:\ruta\a\carpeta
```

## Opciones

Ambos scripts aceptan:

| Opción | Descripción |
| ------ | ----------- |
| `-p CLAVE` | Contraseña directa (si no, se solicita por consola) |
| `-d, --delete` | Borra el archivo original tras cifrar (o el `.enc` tras descifrar) |

Ejemplos:

```
python cifrar.py C:\demo -d -p miClave
python descifrar.py C:\demo -d -p miClave
```

## Comportamiento

- `cifrar.py` convierte cada archivo en `nombre.ext.enc` y crea una nota de rescate (`LEEME_IMPORTANTE.txt`) simulando el mensaje de un ransomware.
- `descifrar.py` restaura el nombre original eliminando el sufijo `.enc`.
- Se usa `-aes-256-cbc -pbkdf2 -salt` para derivar la clave desde la contraseña.

## Diferencias con un ransomware real

- Este script cifra solo el contenido de una carpeta, sin recursividad ni selección de extensiones.
- La clave depende de la contraseña; el ransomware real suele cifrar la clave con la pública del atacante.
- No hay persistencia, propagación ni pago exigido.
