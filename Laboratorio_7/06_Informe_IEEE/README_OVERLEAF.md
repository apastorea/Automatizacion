# Informe IEEE de Laboratorio 7

Formato de artículo académico a dos columnas, coherente con el informe propio del Laboratorio 5. El ejemplo del compañero LM utiliza una columna: se tomó como referencia de **secuencia temática**, no como modelo de resultados.

- Principal: `main.tex`.
- Secciones editables: `secciones/01_introduccion.tex` ... `08_conclusiones.tex`.
- Bibliografía integrada: `secciones/09_bibliografia.tex` para compilar sin BibTeX. Se incluye `referencias.bib` como base para migrar a BibTeX en el futuro; fuentes principales Samanta y Fadali--Visioli, complementadas con Åström--Murray.
- Figuras futuras: `figuras/`; todas deben proceder de MATLAB o del banco, con ejes, unidades y contexto.

En Overleaf: `New Project > Upload Project` (subir un ZIP de esta carpeta solamente) y elegir pdfLaTeX. Puede compilarse localmente:

```bash
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

**No completar las tablas con números de informes ajenos.** Faltan modelo de la planta propio, Ts definitivo, K/Nr/L, datos crudos experimentales, validación de temporización y conclusiones finales cuantitativas. Identidad del estudiante y fecha también están por completar.
