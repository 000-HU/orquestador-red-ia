const { execSync } = require('child_process');
const fs = require('fs');
const readline = require('readline');

// Estética Retro-Linux
const G = "\x1b[32m", B = "\x1b[34m", Y = "\x1b[33m", R = "\x1b[31m", RS = "\x1b[0m";

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

const menu = () => {
    process.stdout.write('\x1bc'); // Clear
    console.log(`${B}╔════════════════════════════════════════════╗${RS}`);
    console.log(`${B}║   BARE-METAL TERMINAL v2.0 - 000-HU        ║${RS}`);
    console.log(`${B}╚════════════════════════════════════════════╝${RS}`);
    console.log(`\n${G}1.${RS} Ejecutar Mapeo de Red (JAVA)`);
    console.log(`${G}2.${RS} Ver Logs de Latencia (JSON)`);
    console.log(`${G}3.${RS} Sincronizar con GitHub (GIT)`);
    console.log(`${G}4.${RS} Salir`);
    process.stdout.write(`\n${Y}root@000-HU:~# ${RS}`);
};

const handleInput = (input) => {
    switch(input.trim()) {
               case '1':
            console.log(`\n${G}[*] Compilando motor Java...${RS}`);
            try {
                execSync('javac RedRecursiva.java');
                const out = execSync('java RedRecursiva').toString();
                
                // Regex avanzado: Extrae latencias y rutas
                const latencias = out.match(/Latencia Total: (\d+)ms/g);
                
                console.log(`\n${B}╔══════════════════════════════════════════╗${RS}`);
                console.log(`${B}║   MONITOR DE LATENCIA (ASCII GRAPH)      ║${RS}`);
                console.log(`${B}╚══════════════════════════════════════════╝${RS}`);

                latencias.forEach((linea, i) => {
                    const ms = parseInt(linea.match(/\d+/));
                    const color = ms < 30 ? G : (ms < 70 ? Y : R);
                    // Dibuja la barra: cada bloque representa 5ms
                    const bloques = "█".repeat(Math.floor(ms / 5));
                    console.log(`Ruta ${i.toString().padStart(2,'0')}: ${color}${bloques}${RS} (${ms}ms)`);
                });
                console.log(`${B}--------------------------------------------${RS}`);
                
            } catch(e) { console.log(`${R}[!] Error en el motor de grafos.${RS}`); }
            break;

        case '2':
            console.log(`\n${B}[*] Leyendo historial...${RS}`);
            if(fs.existsSync('network_state.json')) {
                console.log(fs.readFileSync('network_state.json', 'utf8'));
            } else { console.log(`${R}No hay logs aún.${RS}`); }
            break;
        case '3':
            console.log(`\n${Y}[*] Empujando actualizaciones a la nube...${RS}`);
            try {
                execSync('git add .');
                execSync('git commit -m "Auto-sync from terminal"');
                execSync('git push origin main');
                console.log(`${G}Sincronizado!${RS}`);
            } catch(e) { console.log(`${R}Error de git (quizás no hay cambios)${RS}`); }
            break;
        case '4':
            console.log(`${B}Cerrando sesión...${RS}`);
            process.exit();
        default:
            console.log(`${R}Comando no reconocido.${RS}`);
    }
    setTimeout(() => { menu(); }, 2000);
};

menu();
rl.on('line', handleInput);
