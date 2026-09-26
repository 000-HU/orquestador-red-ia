const axios = require('axios');

async function extraer() {
    try {
        console.log('\n--- CONECTANDO A X PARA ANALIZAR A FATGE7 ---');
        const { data } = await axios.get('https://x.com', {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
        });

        const titulo = data.match(/<title>(.*?)<\/title>/);
        const desc = data.match(/name="description" content="(.*?)"/);
        const id = data.match(/"rest_id":"(\d+)"/);

        console.table({
            'Usuario': titulo ? titulo[1] : 'No encontrado',
            'Biografía': desc ? desc[1] : 'Oculta',
            'ID Numérico': id ? id[1] : 'Necesita Login'
        });

    } catch (e) {
        console.log('⚠️ Error:', e.message);
    }
}

extraer();
