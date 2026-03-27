const oracledb = require('oracledb');

// Configuración Nativa de Oracle UAEMex
const connectionConfig = {
  user: "USUARIO_CONTROL_ESCOLAR", // Cambia por el real
  password: "PASSWORD_DB",         // Cambia por el real
  connectString: "IP_SERVIDOR:1521/SID_ESCOLAR" // Ej: 10.1.2.3:1521/XE
};

async function ejecutarGestion() {
  let conn;
  try {
    conn = await oracledb.getConnection(connectionConfig);
    console.log("[ORACLE] CONEXIÓN EXITOSA A CONTROL ESCOLAR.");

    // Query de ejemplo: Listar facultades registradas en la DB
    const result = await conn.execute(`SELECT * FROM facultades WHERE estatus = 'PARO'`);
    console.table(result.rows);

  } catch (err) {
    console.error("[!] Error de Acceso Oracle:", err.message);
  } finally {
    if (conn) await conn.close();
  }
}

ejecutarGestion();
