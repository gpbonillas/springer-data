# springer-data
Proyecto colaborativo para extraer un dataset desde el portal [Springer](https://www.springer.com/), usando técnicas de Web Scraping. El dataset corresponde a datos bibliográficos de los libros publicados en la página desde el 2015 al 2021 en la disciplina de Ciencias de la Computación.

La estructura general del proyecto es la siguiente:

* src/: Contiene 3 archivos, según las siguientes indicaciones:
  * owner.json: Respuesta JSON al momento de ejecutar el script owner.py
  * owner.py: Script que hace uso de la librería python-whois, lo que permite conocer el propietario de la página.
  * scraper.py: Script que contiene toda la lógica de extracción de los datos del portal de Springer.
* data/: Contiene el dataset luego de haber ejecutado el script scraper.py
* docs/: Contiene la documentación referente al proyecto.
* LICENSE: Contiene la declaración de la licencia usada para este proyecto. En este caso se ha usado la licencia MIT.
* README.md: Contiene una breve descripción del proyecto
