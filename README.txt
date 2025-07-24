# Dividir Lotes (QGIS Plugin)

## 📝 Descripción
Este plugin para QGIS permite **dividir polígonos en parcelas iguales** según atributos de la capa, como:
- `num_lotes`: Número de parcelas en que se subdividirá el polígono.
- `orientacion`: Puede ser `vertical` u `horizontal`.

Ideal para trabajos catastrales, parcelación de terrenos y planificación urbana.

---

## ✅ Características
✔ Divide polígonos en parcelas iguales.  
✔ Soporta múltiples polígonos en una sola ejecución.  
✔ Orientación configurable por atributo.  
✔ Genera una **nueva capa en memoria** con las parcelas resultantes.  

---

## 🔧 Instalación
1. Descarga este repositorio.
2. Copia la carpeta **DividirLotes** en el directorio de plugins de QGIS:
   - **Windows**: `%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins`
   - **Linux**: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins`
3. Reinicia QGIS y activa el plugin desde:
   `Complementos > Administrar e Instalar complementos`

---

## ▶ Uso
1. Selecciona la capa de polígonos.
2. Asegúrate de tener los campos:
   - `num_lotes` → Número de parcelas.
   - `orientacion` → `vertical` o `horizontal`.
3. Ejecuta el plugin y genera las parcelas.

---

## 📌 Autor
**Geografo Edwin Calle Condori**  
📧 eddycc66@gmail.com  

---
