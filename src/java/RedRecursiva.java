import java.util.*;

public class RedRecursiva {
    // Simulación de una red con topología de anillos y malla
    // Nodos: 0:localhost, 1:ssh_gateway, 2:db_sql, 3:firewall, 4:web_server, 5:destino
    static int[][] matrizRed = {
        {0, 10, 20, 0, 0, 0},
        {10, 0, 0, 50, 10, 0},
        {20, 0, 0, 20, 33, 0},
        {0, 50, 20, 0, 20, 2},
        {0, 10, 33, 20, 0, 1},
        {0, 0, 0, 2, 1, 0}
    };

    // Algoritmo de Recursión para encontrar rutas de paquetes
    public static void ruteoRecursivo(int actual, int destino, String camino, int latencia, boolean[] visitado) {
        visitado[actual] = true;
        camino += " -> [" + actual + "]";

        if (actual == destino) {
            System.out.println("Ruta Encontrada: " + camino + " | Latencia Total: " + latencia + "ms");
        } else {
            for (int i = 0; i < matrizRed.length; i++) {
                if (matrizRed[actual][i] > 0 && !visitado[i]) {
                    ruteoRecursivo(i, destino, camino, latencia + matrizRed[actual][i], visitado.clone());
                }
            }
        }
    }

    public static void main(String[] args) {
        System.out.println("\n--- INICIANDO PROTOCOLO DE ANALISIS DE RED ---");
        System.out.println("Origen: localhost (127.0.0.1) | Destino: Nodo Final [5]");
        
        long inicio = System.nanoTime();
        ruteoRecursivo(0, 5, "INICIO", 0, new boolean[matrizRed.length]);
        long fin = System.nanoTime();

        System.out.println("\nOptimización completada en: " + (fin - inicio) / 1000 + " microsegundos.");
        System.out.println("Análisis de topología finalizado.");
    }
}

