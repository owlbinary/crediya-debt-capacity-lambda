# Lambda Capacidad de Endeudamiento

Este proyecto implementa una Lambda en Python 3.12 para calcular la capacidad de endeudamiento de un solicitante, siguiendo arquitectura hexagonal y buenas prácticas.

## Requisitos
- Python 3.12 (recomendado usar conda)
- AWS CLI (opcional, para despliegue)

## Instalación y ambiente de desarrollo

### Usando conda
1. Crear el ambiente:
   ```bash
   conda env create -f environment.yml
   conda activate crediya-debt-capacity-lambda
   ```

### Usando pip
1. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Variables de entorno
- Configura la variable `BASE_URL_SERVICIO_SOLICITUDES` en tu entorno o en `.env` para desarrollo local.
- En AWS Lambda, configura la variable desde la consola.

## Ejecución local
Puedes ejecutar la API localmente con Uvicorn:
```bash
uvicorn app.adapters.api:app --reload
```

## Pruebas y cobertura

### Ejecutar pruebas
Con el entorno activado, ejecuta:
```bash
pytest tests/
```

### Mostrar coverage
Para ver el reporte de cobertura en terminal:
```bash
pytest --cov=app --cov=lambda_handler --cov-report=term-missing tests/
```

Esto mostrará el porcentaje de líneas cubiertas y las líneas faltantes.

## Estructura del proyecto
- `app/domain/` - Lógica de dominio
- `app/application/` - Servicios y casos de uso
- `app/adapters/` - Adaptadores (API, etc)
- `app/infrastructure/` - Infraestructura (repositorios, logger)
