# Tasks  
- Reuniones, Avanzar en trabajo teorico [1 pág], o en cálculos ()
- Implementar programa en linux y armar el workshop (DONE)
- Añadir imagenes de cada institución (DONE)
- Hacer que los datos seriales comiencen cuando presiones el botón baseline, no cuando abra la app (DONE)
- Implementar el baseline para que mida de 400nm a 700nm una sola vez y lo guarde en un arreglo separado (x, y) (DONE)
- Implementar el single para que agarre el baseline, calcule la absorbancia solo una vez (DONE)
- Implementar el continuous para que agarre el baseline, calcule la absorbancia y pueda medir continuamente y hacer stop para pararlo (DONE)
- Implementar el Save Data para guardar datos en un archivo de texto, PDF, etc. (DONE)
- Implementar la pestaña de Settings para ajustes necesarios. (DONE)
- Implementar la barra de medición el cuál aumenta mientras va calculando. (DONE)
- Implementar labels o textos de los valores de las gráficas al finalizar y valores específicos. (DONE)
- Funcion para ver unidad de absorcion en un punto especifico en la grafica, (Escribir longitud de onda y obtener su absorbancia) (DONE)
- Agregar mensajes de (Baseline listo, absorbancia calculada, calculando absorbancia continua) (DONE)
- Poner los datos de la medicion en pantalla en otro tab (DONE)
- Si se comienza a medir mal, no medir en lo absoluto (hacer 5 sweeps iniciales, el 1 siempre sale mal) (DONE)
- Una vez realizada la calibración y apuntar ajustes, hacer la intrapolación para tener medidas en cada longitud de onda, no cada 2 o 3 nm. (DONE, REALIZADO EN SHOW DATA)
- Hacer interpolación en Select Wavelength y datos de save data (DONE)

# Web Server Tasks
- Crear la página web (DONE)
- Crear los módulos dentro de la página web [Gráficas, Datos, Archivos, User] (DONE)
- Implementar módulo de últimas mediciones (archivos y gráficas) en dashboard, con estadisticas (# mediciones, tipos de archivos) (DONE)
- Implementar módulo de datos (DONE)
- Implementar modulo de gráfica (DONE)
- Implementar modulo de archivos (DONE)
- Añadirle un módulo de acceso al portal ()
- Integrar el POST/REQUEST para que se comunique con el equipo (DONE)
- Enviar los datos al portal desde el equipo (CSV, PNG, SVG, PDF) (DONE)
- Implementar pestaña de usuario ()
- Mejorar la vista del módulo de datos (DONE)
- Mejorar la vista del módulo de archivos (DONE)
- Mejorar la vista del módulo de gráficas (DONE)
- Subir página web al internet con su dominio y hosting único (DONE)

# Tasks requeridos por el asesor
1. Maximo y minimo de la grafica (DONE) 
2. Rango de interes (Selección de rango de dos puntos en donde la grafica se auto ajusta dar valores para cada nm?) (DONE)
3. Autoscale (Modificar las medidas iniciales que dan por 890) (DONE)
4. Span configurable (Rango), Center wavelength, Longitud de onda mayor y menor (DONE)
5. Zoom manual en la grafica (DONE, SE USA EL SPAN)
6. Graficar lineal y no lineal (Logaritmica) (DONE)
7. Agregar dB en la grafica de absorbancia y en la de intensidad U.A (DONE)
8. Guardar datos en archivo para graficar (TXT, WAVELENGTH, ABSORBANCE) (DONE)
9. Diseñar para pantalla de 10 pulgadas (DONE)
10. Agregar datos estadísticos en el PDF (DONE)
11. Cambiar los parámetros fotometricos y agregar los radiometricos (DONE)
12. Agregar un tabs (parameters, about, etc) para ver los datos como en el PDF (DONE)
13. Invertir la curva (DONE)
14. Suavizar la curva (DONE)
15. Poder hacer baseline mas de una vez (DONE)
16. Añadir ventilador que extraiga aire de dentro del equipo (DONE, SE TIENE UNA ABERTURA EN EL DISEÑO)
17. Hacer ecuaciones cúbicas para longitudes de onda espécificas (DONE)
18. Poner el logo del SNI (DONE)
19. Poner en PDF en primera página si el liquido está contaminado (DONE)
20. Reducir tamaño ancho de la línea de la gráfica (DONE)
21. Ajustar a diferentes tipos de gráficas [Gausiana, Lorentziana, 1er-4to orden] (DONE)
22. Hacer el Tab para determinar si el MTV está contaminado (DONE)
23. Automáticamente ir haciendo sweeps de baseline hasta que comience la medición con 152 a 156 [Inicios inconsistentes del equipo] ()
24. Repaso final de las funciones y ver que funciona y que no ()
25. Implementación de usar referencias para luego medir sustancias contaminadas de esa referencia ()
