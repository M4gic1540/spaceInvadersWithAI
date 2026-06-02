# Space Invaders: Evolución por Algoritmo Genético e IA Matricial

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.0+-green?style=for-the-badge&logo=pygame&logoColor=white)
![Git](https://img.shields.io/badge/Git-Flow-orange?style=for-the-badge&logo=git&logoColor=white)

Este proyecto es una simulación evolutiva basada en el clásico juego *Space Invaders*. En esta versión, los alienígenas no siguen patrones de movimiento rígidos o preprogramados; en su lugar, cada individuo posee un **cerebro artificial autónomo** que evoluciona dinámicamente mediante un **Algoritmo Genético (GA)** para aprender a sobrevivir a los ataques del jugador.

---

## 🧠 Arquitectura de la Inteligencia Artificial

A diferencia de las aproximaciones lineales simples, este proyecto implementa un **Perceptrón Multicapa (MLP)** que permite a los agentes procesar abstracciones complejas del entorno.

### 1. Sistema Sensorial (Capa de Entrada)
Cada alienígena evalúa constantemente un vector de 4 entradas normalizadas continuas:
* **`dist_jugador`** $[-1.0, 1.0]$: Posición horizontal relativa respecto a la nave del jugador.
* **`bala_x`** $[-1.0, 1.0]$: Desplazamiento horizontal de la bala más cercana en su carril de peligro.
* **`bala_y`** $[0.0, 1.0]$: Proximidad vertical del proyectil (donde $0.0$ es impacto inminente).
* **`dist_borde`** $[-1.0, 1.0]$: Ubicación relativa respecto a los límites físicos de la pantalla.

### 2. Procesamiento No Lineal (Capa Oculta)
La red cuenta con una capa oculta de **4 neuronas** interconectadas mediante matrices de pesos y sesgos ($4 \times 4$). Utiliza la función de activación **Tangente Hiperbólica (Tanh)**:

$$f(x) = \tanh(x)$$

Esto permite comprimir las señales entre $[-1.0, 1.0]$, logrando que la IA aprenda relaciones abstractas como *"esquivar solo si la bala está cerca Y tengo espacio disponible hacia el borde"*.

### 3. Toma de Decisiones (Capa de Salida)
La red reduce la información a un único nodo de salida que se mapea discretamente en tres estados mecánicos de hardware:
* $<-0.3 \rightarrow$ Desplazamiento a la **Izquierda** (`-1`)
* $>0.3 \rightarrow$ Desplazamiento a la **Derecha** (`1`)
* $\text{Otro} \rightarrow$ Mantenerse **Inmóvil** (`0`)

---

## ⚙️ Características Principales

* **Algoritmo Genético Puro**: Al finalizar cada oleada, el sistema calcula el *Fitness* biológico de cada espécimen en función de sus frames de supervivencia. Los cerebros élite son seleccionados y clonados aplicando **mutaciones gaussianas incrementales** en sus matrices sinápticas.
* **Modo Sparring Automático (Granja de Entrenamiento)**: El proyecto incluye un piloto automático heurístico para el jugador. Al activarse, la nave persigue y dispara ráfagas constantes sin fatiga, permitiendo ejecutar el bucle de Pygame en modo *fast-forward* (`reloj.tick(0)`) para avanzar cientos de generaciones en minutos.
* **Persistencia de Especies (JSON)**: Implementa métodos avanzados de serialización y deserialización matricial. Los mejores cerebros de la historia se guardan automáticamente en un archivo `cerebros_elite.json`, permitiendo pausar el entrenamiento y reanudarlo preservando el conocimiento evolutivo.
* **Diseño Modular POO**: Estructura de código limpia basada en herencia de entidades (`Jugador`, `Alien`, `Proyectil` heredan de una clase `Entidad` base), garantizando un desacoplamiento óptimo entre el motor de física y los módulos de IA.

---

## 📂 Estructura del Proyecto

```text
├── entidades/
│   ├── base.py          # Clase Entidad con lógicas de rect y render
│   ├── jugador.py       # Lógica del jugador (Manual / Autopilot Sparring)
│   ├── alien.py         # Agente evolutivo conectado a la Red Neuronal
│   └── proyectil.py     # Física de los disparos
├── ia/
│   └── cerebro.py       # Red Neuronal Multicapa (MLP) y lógicas del GA
├── data/
│   └── cerebros_elite.json # Almacenamiento de matrices de pesos óptimos
├── main.py              # Bucle principal de Pygame y control de generaciones
└── README.md