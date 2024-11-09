const express = require('express');
const bodyParser = require('body-parser');
const fetch = require('node-fetch');
const cors = require('cors');

const app = express();
const PORT = 3000;

app.use(cors());
app.use(bodyParser.json());

const OPENAI_API_KEY = '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'; // Используйте свой реальный API-ключ

app.post('/api/chat', async (req, res) => {
    const fullName = req.body.fullName; // Получаем полное имя из запроса

    if (!fullName) {
        return res.status(400).json({ error: 'Полное имя отсутствует.' });
    }

    try {
        const response = await fetch('https://api.openai.com/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${OPENAI_API_KEY}`,
            },
            body: JSON.stringify({
                model: 'gpt-3.5-turbo',
                messages: [{ role: 'user', content: `Привет, меня зовут ${fullName}. Как вы можете мне помочь?` }],
            }),
        });

        if (!response.ok) {
            const errorBody = await response.text();
            return res.status(response.status).json({ error: errorBody });
        }

        const data = await response.json();
        res.json({ message: data.choices[0].message.content }); // Возвращаем ответ клиенту
    } catch (error) {
        console.error('Ошибка:', error);
        res.status(500).send('Ошибка при обращении к OpenAI');
    }
});

app.listen(PORT, () => {
    console.log(`Сервер запущен на http://localhost:${PORT}`);
});