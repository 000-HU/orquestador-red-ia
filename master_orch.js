console.log("🚀 [Master Orch] Inicializando hackeo de interfaz gráfica en el DOM...");

// 1. Inyección de estilos de ciberseguridad directamente en la cabecera de la página UAEMex
const estilos = document.createElement('style');
estilos.innerHTML = `
    #zero-overlay-dashboard {
        position: fixed;
        top: 20px;
        right: 20px;
        width: 380px;
        max-height: 85vh;
        background: rgba(10, 15, 29, 0.95);
        color: #e2e8f0;
        border: 2px solid #38bdf8;
        border-radius: 12px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.7);
        z-index: 999999;
        font-family: 'Segoe UI', Roboto, sans-serif;
        padding: 20px;
        display: flex;
        flex-direction: column;
        backdrop-filter: blur(10px);
    }
    .zero-header {
        border-bottom: 2px solid #141b2d;
        padding-bottom: 10px;
        margin-bottom: 15px;
    }
    .zero-header h2 { margin: 0; font-size: 18px; color: #38bdf8; }
    .zero-content {
        overflow-y: auto;
        flex-grow: 1;
    }
    .zero-card {
        background: #141b2d;
        border-left: 4px solid #ef4444;
        padding: 10px;
        border-radius: 6px;
        margin-bottom: 10px;
    }
    .zero-card h4 { margin: 0 0 5px 0; font-size: 14px; color: #f97316; }
    .zero-card p { margin: 2px 0; font-size: 12px; opacity: 0.8; }
`;
document.head.appendChild(estilos);

// 2. Creación del contenedor del Dashboard en el árbol del DOM
const dashboard = document.createElement('div');
dashboard.id = 'zero-overlay-dashboard';
dashboard.innerHTML = `
    <div class="zero-header">
        <h2>🤖 Sistema Zero: Core IA</h2>
        <small style="opacity: 0.5;">Auditoría de Red Integrada en DOM</small>
    </div>
    <div class="zero-content" id="zero-alertas-container">
        <p style="text-align: center; opacity: 0.6;">Cargando telemetría de red...</p>
    </div>
`;
document.body.appendChild(dashboard);

// 3. Consulta asíncrona real a tu puerto 3001
async function mapearDatosEnDOM() {
    try {
        const respuesta = await fetch('http://localhost:3001/api/anomalias');
        const anomalias = await respuesta.json();
        const contenedor = document.getElementById('zero-alertas-container');
        contenedor.innerHTML = '';

        if (anomalias.length === 0) {
            contenedor.innerHTML = '<p style="color:#10b981; text-align:center;">✔️ Red limpia. Sin anomalías estadísticas.</p>';
            return;
        }

        anomalias.forEach(alerta => {
            const card = document.createElement('div');
            card.className = 'zero-card';
            card.innerHTML = `
                <h4>🎯 Host Detectado: ${alerta.IP}</h4>
                <p><strong>Desviación:</strong> ${alerta.Metrica_Desviacion.toFixed(2)} octetos</p>
                <p style="font-size: 11px; color: #ef4444; margin-top: 5px;">⚠️ ${alerta.Estatus}</p>
            `;
            contenedor.appendChild(card);
        });
        console.log("✅ [DOM] Interfaz del Sistema Zero actualizada dinámicamente.");
    } catch (error) {
        document.getElementById('zero-alertas-container').innerHTML = `<p style="color:#ef4444;">❌ Error de enlace con el puerto 3001</p>`;
    }
}

// Ejecutar mapeo
mapearDatosEnDOM();
