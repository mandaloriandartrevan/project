const express = require('express');
const app = express();
const server = require('http').createServer(app);

app.use(express.json());

app.post('/send_activity', (req, res) => {
    // Логика обработки запроса о рабочей активности
    // Ваш код для отправки данных на сервер
    res.send("Activity data sent to server");
});

app.post('/send_screenshot', (req, res) => {
    // Логика для сохранения скриншота на сервере
    // Ваш код для сохранения скриншота
    res.send("Screenshot sent to server");
});

server.listen(8888, () => {
    console.log('Server is running on port 8888');
});
