# Dataset books_data_springer

## Descripción del proyecto
Proyecto colaborativo para extraer un dataset desde el portal [Springer](https://www.springer.com/), usando técnicas de Web Scraping. El dataset corresponde a datos bibliográficos de los libros publicados en el portal desde el 2015 al 2021, en la disciplina de Ciencias de la Computación.

## Componentes del grupo

| Contribuciones   | Firma  |
|------------------|--------|
| Investigación previa  | L.A.T.G., G.P.B.S. |
| Redacción de las respuestas  | L.A.T.G., G.P.B.S. |
| Desarrollo código  | L.A.T.G., G.P.B.S.  |

## Descripción de ficheros
La estructura general del proyecto es la siguiente:

* **src**: Esta carpeta contiene 3 archivos, según las siguientes indicaciones:
  * **owner.json**: Respuesta JSON al momento de ejecutar el script owner.py
  * **owner.py**: Script que hace uso de la librería python-whois, lo que permite conocer el propietario de la página.
  * **scraper.py**: Script que contiene toda la lógica de extracción de los datos del portal de Springer.
* **data**: Contiene el dataset books_data_springer.csv luego de haber ejecutado el script scraper.py
* **docs**: Contiene la documentación referente al proyecto.
* **LICENSE**: Archivo que contiene la declaración de la licencia usada para este proyecto. En este caso se ha usado la licencia MIT.
* **README.md**: Archivo que contiene una breve descripción del proyecto

## Ejecución del script
Para ejecutar los scripts del proyecto es necesario instalar las siguientes librerías:

```python
pip install requests
pip install beautifulsoup4
pip install python-whois
```

## Información adicional
Para mayor información del proyecto visite la [Wiki Oficial](https://github.com/gpbonillas/springer-data/wiki)

## Publicación del dataset
El DOI del dataset publicado en Zenodo es: [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4683793.svg)](https://doi.org/10.5281/zenodo.4683793)

