const express = require('express');
const path = require('path');
const app = express();
const PORT = 8080;

// Servir la carpeta de evidencias
app.use('/descargas', express.static(path.join(__dirname, 'paro_uaemex')));

app.get('/', (req, res) => {
    res.send(`
        <body style="background:#003121; color:#d4af37; font-family:sans-serif; padding:40px;">
            <h1 style="border-bottom:2px solid #d4af37;">🏛️ REPOSITORIO DE TRANSPARENCIA - PARO UAEMEX 2026</h1>
            <div style="background:#fff; color:#333; padding:20px; border-radius:10px;">
                <h2>Estatus del Plantón: ACTIVO</h2>
                <p>Evidencia técnica y comunicados oficiales del movimiento estudiantil.</p>
                <a href="/descargas" style="display:inline-block; background:#d4af37; color:#003121; padding:15px; text-decoration:none; font-weight:bold; border-radius:5px;">
                    ACCEDER AL DIRECTORIO DE ARCHIVOS
                </a>
            </div>
            <p style="font-size:0.8em; margin-top:20px;">Difusión descentralizada - Bare-Metal UAEMex</p>
        </body>
    `);
});

app.listen(PORT, () => {
    console.log(`[BARE-METAL] Servidor UAEMex reestablecido en Puerto ${PORT}`);
});
