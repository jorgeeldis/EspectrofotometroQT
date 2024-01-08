# Tasks 
- Implementar programa en linux y armar el workshop (DONE)
- Añadir imagenes de cada institución
- Hacer que los datos seriales comiencen cuando presiones el botón baseline, no cuando abra la app (DONE)
- Implementar el baseline para que mida de 400nm a 700nm una sola vez y lo guarde en un arreglo separado (x, y)
- Implementar el single para que agarre el baseline, calcule la absorbancia solo una vez
- Implementar el continuous para que agarre el baseline, calcule la absorbancia y pueda medir continuamente  y hacer stop para pararlo
- Implementar el Save Data para guardar datos en un archivo de texto.
- Implementar la pestaña de Settings para ajustes necesarios.
- Implementar la barra de medición el cuál aumenta mientras va calculando.
- Implementar valores de las gráficas al finalizar y valores específicos.
- Funcion para ver unidad de absorcion en un punto especifico en la grafica, (Escribir longitud de onda y obtener su absorbancia)
- Agregar mensajes de (Baseline listo, absorbancia calculada, calculando absorbancia continua)
- Funcionalidad para apagar el LED desde python en otro tab
- Poner los datos de la medicion en pantalla en otro tab
- En el boton de save data tener un dropdown para guardar en PC, Email, TXT, Etc (Crear informe con datos de lecturas)
- Agregar una luz para indicar si hay error o esta midiendo o esta listo

# Tasks requeridos por el asesor
1. Maximo y minimo de la grafica 
2. Resta entre dos gráficas en paralelo
3. Rango de interes (Rango de dos puntos en donde la grafica difiere del 0)
4. Autoscale (Modificar las medidas iniciales que dan por 890)
5. Span configurable (Rango), Center wavelength, Longitud de onda mayor y menor
6. Zoom manual en la grafica
7. Graficar lineal y no lineal (Logaritmica) 
8. Usar fuente para LED, calcular su intensidad par la resistencia
9. Agregar dB en la grafica de absorbancia y en la de intensidad U.A
10. Guardar datos en archivo para graficar (TXT, WAVELENGTH, ABSORBANCE)
11. Promediado con cuantos sweeps (Cuantas veces se grafica y se promedia entre esas medidas)
12. Variar intensidad del led (Fuente de 12V) (PWM) (Filtro de primer orden) 360mA
13. Diseñar para pantalla de 10 pulgadas
14. Ver lo de continuo, da problemas
15. Poder hacer baseline mas de una vez