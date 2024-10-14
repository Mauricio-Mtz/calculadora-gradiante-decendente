const express = require('express');
const { exec } = require('child_process');
const path = require('path'); // Para manejar rutas correctamente
const app = express();
const port = 3000;

// Middleware para parsear JSON
app.use(express.json()); 

// Servir archivos estáticos desde la carpeta 'public'
app.use(express.static(path.join(__dirname, 'public')));

// Ruta para ejecutar el código Python y enviar la respuesta al navegador
app.post('/solve', (req, res) => {
  // Extraer los valores de las ecuaciones desde la solicitud
  const { m, b, o, coordinates } = req.body;

  console.log('Datos recibidos:', { m, b, o, coordinates });

  // Validar que todos los valores estén presentes
  if (!m || !b || !o || !coordinates || !Array.isArray(coordinates)) {
    return res.status(400).json({ error: 'Faltan datos o las coordenadas no son válidas' });
  }

  // Serializa las coordenadas como una lista de valores x y y
  const coordString = coordinates.map(coord => `${coord.x} ${coord.y}`).join(' ');

  // Ejecutar el script de Python con los valores de m, b, o y las coordenadas
  exec(`python solve.py ${m} ${b} ${o} ${coordString}`, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error ejecutando Python: ${error}`);
      console.error(`stderr: ${stderr}`);
      return res.status(500).json({ error: 'Error ejecutando Python' });
    }

    try {
      const result = JSON.parse(stdout);  // Intenta parsear la salida como JSON
      res.json(result);  // Responde con el resultado en JSON
    } catch (parseError) {
      console.error('Error parseando JSON:', parseError);
      res.status(500).json({ error: 'Error parseando la respuesta de Python' });
    }
  });
});

// Iniciar el servidor
app.listen(port, () => {
  console.log(`Servidor escuchando en http://localhost:${port}`);
});
