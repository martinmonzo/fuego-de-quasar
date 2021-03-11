# Operación Fuego de Quasar

Han Solo ha sido recientemente nombrado General de la Alianza Rebelde y busca dar un gran golpe contra
el Imperio Galáctico para reavivar la llama de la resistencia.

El servicio de inteligencia rebelde ha detectado un llamado de auxilio de una nave portacarga imperial
a la deriva en un campo de asteroides. El manifiesto de la nave es ultra clasificado, pero se rumorea
que transporta raciones y armamento para una legión entera.

**Contenido**

- [Operación Fuego de Quasar](#operación-fuego-de-quasar)
  - [Ubicación del proyecto y cómo ejecutarlo](#ubicación-del-proyecto-y-cómo-ejecutarlo)
    - [Ejecución desde la web](#ejecución-desde-la-web)
    - [Ejecución desde Postman](#ejecución-desde-postman)
  - [Documentación acerca del proyecto](#documentación-acerca-del-proyecto)
    - [1. /topsecret/](#1-topsecret)
      - [POST -> /topsecret/](#post---topsecret)
        - [Payload](#payload)
        - [Success Response](#success-response)
        - [Error Response](#error-response)
    - [2. /topsecret_split/{satellite_name}](#2-topsecret_splitsatellite_name)
      - [POST -> /topsecret_split/{satellite_name}](#post---topsecret_splitsatellite_name)
        - [Payload](#payload-1)
        - [Response](#response)
      - [GET -> /topsecret_split/{satellite_name}](#get---topsecret_splitsatellite_name)
        - [Success Response](#success-response-1)
        - [Error Response](#error-response-1)
  - [Descripción del problema](#descripción-del-problema)
  - [Demostración de la fórmula](#demostración-de-la-fórmula)
  - [Consideraciones a tener en cuenta](#consideraciones-a-tener-en-cuenta)
    - [1. Aproximación de valores](#1-aproximación-de-valores)
    - [2. Base de Datos](#2-base-de-datos)

---
## Ubicación del proyecto y cómo ejecutarlo
El proyecto se encuentra hosteado en este [link](https://quasarfireapp-mmonzo.herokuapp.com/topsecret) en Heroku.

Se puede ejecutar directamente desde la web, o mediante alguna aplicación para testear APIs, como por ejemplo Postman.

### Ejecución desde la web
1. **POST -> /topsecret/**:
   1. Abrir https://quasarfireapp-mmonzo.herokuapp.com/topsecret
   2. Seleccionar la opción **Raw data**
   3. Pegar el payload en el campo Content del formulario de Post, con el mismo formato que se indica [aquí](#payload)
2. **POST -> /topsecret_split/{satellite_name}**:
   1. Abrir https://quasarfireapp-mmonzo.herokuapp.com/topsecret_split/kenobi
   2. Seleccionar la opción **Raw data**
   3. Pegar el payload en el campo Content del formulario de Post, con el mismo formato que se indica [aquí](#payload-1).
   - TENER EN CUENTA QUE EL **{satellite_name}** PUEDE SER:
     - kenobi
     - skywalker
     - sato
3. **GET -> /topsecret_split/{satellite_name}**:
   1. Abrir https://quasarfireapp-mmonzo.herokuapp.com/topsecret_split/kenobi y podrá observarse la respuesta directamente, dado que el método es un **GET** y no requiere payload.
   - TENER EN CUENTA QUE NO HABRÁ SUFICIENTE INFORMACIÓN HASTA QUE HAYA INFORMACIÓN EN LA BASE DE DATOS ACERCA DE LA DISTANCIA DEL TRANSMISOR A CADA SATÉLITE Y DE CADA MENSAJE RECIBIDO POR LOS SATÉLITES. Esto es posible de 2 maneras:
     1. Ejecutando 1 **POST -> /topsecret_split/{satellite_name}** a cada satélite antes de ejecutar el GET.
     2. Ejecutar **POST -> /topsecret/** una sola vez, dado que este método actualiza los valores en la Base de Datos.

### Ejecución desde Postman
1. **POST -> /topsecret/**:
   1. Pegar el link https://quasarfireapp-mmonzo.herokuapp.com/topsecret en el campo de **URL**
   2. Seleccionar el método **POST**
   3. Pegar el payload en el formulario de **body** con el mismo formato que se indica [aquí](#payload)
2. **POST -> /topsecret_split/{satellite_name}**:
   1. Pegar el link https://quasarfireapp-mmonzo.herokuapp.com/topsecret_split/kenobi
   2. Pegar el payload en el campo Content del formulario de Post, con el mismo formato que se indica [aquí](#payload-1).
3. **GET -> /topsecret_split/{satellite_name}**:
   1. Pegar el link https://quasarfireapp-mmonzo.herokuapp.com/topsecret_split/kenobi
   2. Seleccionar el método **GET**
## Documentación acerca del proyecto
El proyecto consiste en el desarrollo de los siguientes endpoints:

### 1. /topsecret/
   El servicio recibe la **distancia** desde el transmisor a cada uno de los satélites, junto con el **mensaje** recibido por cada satélite.

   Devuelve la **posición (X,Y)** del transmisor y el **mensaje original** enviado por este a los satélites.
   Además, guarda estos valores en la Base de Datos.
   
   #### POST -> /topsecret/

   ##### Payload
  
      {
         "satellites": [
            {
               "name": "kenobi",
               "distance": 100,
               "message": ["Este", "", "", "mensaje", ""]
            },
            {
               "name": "skywalker",
               "distance": 115.5,
               "message": ["", "es", "", "", "secreto"]
            },
            {
               "name": "sato",
               "distance": 142.7,
               "message": ["este", "", "un", "", ""]
            }
         ]
      }

   ##### Success Response

      RESPONSE CODE: 200

      {
         "position": {
            "x": -100.0,
            "y": 75.5
         },
         "message": "este es un mensaje secreto"
      }

   ##### Error Response

      RESPONSE CODE: 404

### 2. /topsecret_split/{satellite_name}
   El servicio acepta **POST** y **GET**:

   #### POST -> /topsecret_split/{satellite_name}
   Recibe la **distancia** desde el transmisor a UNO de los satélites (aquel cuyo nombre es {satellite_name}), junto con el **mensaje** recibido por este satélite.

   Devuelve un **status=200** si la información recibida es válida y se pudo actualizar en la Base de Datos.

   ##### Payload
           
      {     
         "distance": 100,
         "message": ["este", "", "", "mensaje", ""]
      }

   ##### Response

      RESPONSE CODE: 200

   #### GET -> /topsecret_split/{satellite_name}
   Devuelve la **posición (X,Y)** del transmisor y el **mensaje original** enviado por este, siempre y cuando ya se haya registrado una **distancia** y **mensaje** desde el transmisor hacia cada uno de los satélites.

   ##### Success Response

      RESPONSE CODE: 200

      {
         "position": {
            "x": -100.0,
            "y": 75.5
         },
         "message": "este es un mensaje secreto"
      }

   ##### Error Response

      RESPONSE CODE: 404
      
      {
         'error': 'There is no enough information.
      }

## Descripción del problema
El problema principal radica en determinar la **posición (X,Y)** del transmisor, en base a la distancia de este hacia cada uno de los 3 satélites. Para resolverlo, se debe emplear un cálculo de trilateración, mediante el cual se va descubriendo paso a paso las posibles ubicaciones del transmisor, hasta llegar a descubrir la ubicación exacta (**siempre que sea posible**).

1. Al conocer la distancia desde el transmisor hasta el 1er satélite, se determina una circunferencia cuyo radio es igual a esta distancia. El transmisor puede encontrarse en cualquier punto dentro de esta circunferencia.
2. Al conocer la distancia desde el transmisor hasta el 2do satélite, se determina una nueva circunferencia cuyo radio es igual a esta distancia. Por lo tanto, hay 2 opciones:
   1. Si ambas circunferencias se tocan entre sí, lo harán en 2 puntos distintos. Por lo tanto, el transmisor puede encontrarse en cualquiera de estos 2 puntos.
   2. Si las circunferencias no tienen ningún punto en común, el sistema no tiene solución.
3. Suponiendo que las circunferencias de 1. y 2. comparten puntos en común, ahora se conoce la distancia desde el transmisor hasta el 3er satélite, lo cual determina una nueva circunferencia cuyo radio es igual a esta distancia. Por lo tanto, hay 2 opciones:
   1. Si la nueva circunferencia contiene a uno de los 2 puntos en cuestión, este punto es la solución del problema - **posición (X,Y) del transmisor**.
   2. En caso contrario, el sistema no tiene solución.

## [Demostración de la fórmula](https://github.com/martinmonzo/fuego-de-quasar/blob/main/docs/Trilateraci%C3%B3n.pdf)

## Consideraciones a tener en cuenta

### 1. Aproximación de valores
Debido a que se opera las fórmulas empleadas dan como resultado un punto **(X,Y)** que puede ser o no ser solución del sistema, se debe chequear que este punto se encuentre efectivamente a la distancia especificada de cada uno de los satélites.

Como sabemos, la fórmula para determinar la distancia entre un punto **(X,Y)** y un punto **(X1,Y1)** es
**(X-X1)^2+(Y-Y1)^2 = r^2**, siendo **r** la distancia entre ambos puntos. Por lo tanto, debemos asegurarnos que el punto **(X,Y)** devuelto por la fórmula cumpla con esto para cada uno de los satélites.

Sin embargo, como se opera con numeros reales, los decimales son rellenados con datos inexactos, y esta igualdad podría verse afectada. Es por esto que determinaremos esta "igualdad" con un factor de tolerancia (en nuestro caso, sera de **1e-3 = 0.0001**).

### 2. Base de Datos
Para ejecutar el método **GET -> /topsecret_split/{satellite_name}** y obtener una respuesta exitosa, es necesario que las **distancias** desde el transmisor hacia todos los satélites sea conocida, al igual que el **mensaje** recibido por cada uno de ellos. Para que esto sea posible, necesitaríamos ejecutar primero al menos 3 veces el método **POST -> /topsecret_split/{satellite_name}** (una vez por cada satélite).

Para evitar esto, la implementación del método **POST -> /topsecret/** guarda estos valores en la Base de Datos para cada satélite, de modo de evitar tener que ejecutar 3 veces un método antes de poder ejecutar exitosamente **GET -> /topsecret_split/{satellite_name}**.

Por lo tanto, es suficiente con ejecutar una vez **POST -> /topsecret/** para poder hacer un **GET**.


