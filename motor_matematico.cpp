#include <iostream>
#include <vector>
#include <cmath>
#include <numeric>

// Función exportable o ejecutable para análisis de anomalías de red
void analizarAnomalias(const std::vector<int>& trafico) {
    if (trafico.empty()) return;

    // 1. Calcular la Media Matemática
    double suma = std::accumulate(trafico.begin(), trafico.end(), 0.0);
    double media = suma / trafico.size();

    // 2. Calcular la Desviación Estándar
    double sumaVarianza = 0.0;
    for (int pps : trafico) {
        sumaVarianza += std::pow(pps - media, 2);
    }
    double desviacionEstandar = std::sqrt(sumaVarianza / trafico.size());

    std::cout << "[C++] Media de trafico: " << media << " pps" << std::endl;
    std::cout << "[C++] Desviacion Estandar: " << desviacionEstandar << std::endl;

    // 3. Umbral de Anomalía Asimétrica (Cisne Negro)
    double threshold = 2.0; 
    for (size_t i = 0; i < trafico.size(); ++i) {
        double zScore = (trafico[i] - media) / (desviacionEstandar == 0 ? 1 : desviacionEstandar);
        if (std::abs(zScore) > threshold) {
            std::cout << "[!] CRITICO en Indice " << i << ": " << trafico[i] 
                      << " pps detectados. Z-Score: " << zScore << std::endl;
        }
    }
}

int main() {
    std::cout << "[*] Iniciando Motor Binario Puro C++ para Orquestador IA..." << std::endl;
    // Datos de ejemplo simulando ráfagas en la pila de red (network_state)
    std::vector<int> datosTrafico = {45, 52, 48, 120, 50, 47, 53, 200, 46};
    analizarAnomalias(datosTrafico);
    return 0;
}
