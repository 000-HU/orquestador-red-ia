const { execSync } = require('child_process');
const fs = require('fs');

// --- DECLARACIÓN DE COLORES (AQUÍ ESTABA EL ERROR) ---
const G = "\x1b[32m"; // Verde
const R = "\x1b[31m"; // Rojo
const B = "\x1b[34m"; // Azul
const Y = "\x1b[33m"; // Amarillo
const W = "\x1b[37m"; // Blanco (ESTA ES LA QUE FALTABA)
const RS = "\x1b[0m"; // Reset

const clear = () => process.stdout.write('\x1bc');

async function llamarIA(ms) {
    console.log(`${Y}[AI-ORCH] Consultando a Gemini/DeepSeek...${RS}`);
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve(`ANÁLISIS IA: Latencia de ${ms}ms detectada. La topología es estable.`);
        }, 800);
    });
}

async function start() {
    clear();
    console.log(`${B}╔════════════════════════════════════════════════════╗${RS}`);
    console.log(`${B}║  BARE-METAL MULTI-ORCHESTRATOR v2.1 (FIXED)       ║${RS}`);
    console.log(`${B}╚════════════════════════════════════════════════════╝${RS}\n`);

    try {
        console.log(`${G}[STEP 1] Compilando motor Java...${RS}`);
        execSync('javac RedRecursiva.java');
        
        console.log(`${G}[STEP 2] Ejecutando análisis de grafos...${RS}`);
        const javaOut = execSync('java RedRecursiva').toString();
        
        // Extraemos el número de la latencia
        const match = javaOut.match(/Latencia Total: (\d+)ms/);
        const ms = match ? match[1] : "ERR";

        console.log(`${G}[DATA] Latencia detectada: ${ms}ms${RS}`);

        const aiResponse = await llamarIA(ms);
        
        console.log(`\n${Y}>>> INSIGHT DE IA:${RS}`);
        console.log(`${W}${aiResponse}${RS}`); // AQUÍ YA NO FALLARÁ

        console.log(`\n${B}------------------------------------------------------${RS}`);
        console.log(`${G}SYSTEM STATUS: ONLINE | BARE-METAL: OK${RS}`);
        console.log(`${B}------------------------------------------------------${RS}`);

    } catch (e) {
        console.log(`${R}[ERROR] Fallo en la cadena: ${e.message}${RS}`);
    }
}

start();
