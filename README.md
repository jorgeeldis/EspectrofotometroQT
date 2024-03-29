# EspectrofotometroQT V1.0

## Instalación

1. Dentro del directorio (EspectrofotometroQT) montar el ambiente virtual con el comando `python -m venv venv`
2. Activar el ambiente virtual con el comando `venv\Scripts\activate` o `source venv\bin\activate`
3. Instalar las dependencias con el comando `pip install -r requirements.txt` que están en el directorio src
4. Ejecutar el archivo main.py con el comando `python main.py` como prueba.

## Sitios para referencias

- [PyGraph](https://www.pyqtgraph.org/)
- [Documentación de ejemplo](https://www.hardware-x.com/article/S2468-0672(20)30016-X/fulltext)
- [Documentación y Hardware](https://osf.io/qv57d)
- [Ejemplo del Python](https://cdn.hackaday.io/files/12491534414944/pyqt_spec_ser.py)

## El designer de WQ está en el directorio

1. venv\Lib\site-packages\qt5_applications\Qt\bin\designer.exe  # Para windows
2. Crear un acceso directo en el escritorio

## Diseñador QT
- [Documentación de ejemplo del diseñador de QT](https://realpython.com/qt-designer-python/#installing-and-running-qt-designer)

## Convertir .ui a .py
$ pyuic5 -o main_window_ui.py ui/main_window.ui

## Ejecutar la aplicación de ejemplo

1. Activar el ambiente virtual con el comando `venv\Scripts\activate`
2. Entrar al directorio test-qt y ejecutar el comando `python ejemplo_ui.py`

## Nota

- El archivo app.py tiene un ejemplo de comunicación por el puerto serial y grafica en tiempo real.

## Bug para derivar gráfica

- Se agrega esta funcion en el archivo PlotItem.py:

def setDerivativeMode(self, state):
        """
        ``state = True`` enables derivative mode, where a mapping according to
        ``y_mapped = dy / dx`` is applied, with `dx` and `dy` representing the 
        differences between adjacent `x` and `y` values.
        """
        if state is not None:
            self.ctrl.derivativeCheck.setChecked(state)