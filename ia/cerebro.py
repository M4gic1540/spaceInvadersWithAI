import random
import math


class CerebroAlien:
    def __init__(
        self,
        pesos_entrada_oculta=None,
        bias_oculto=None,
        pesos_oculta_salida=None,
        bias_salida=None,
    ):
        """
        Arquitectura Red Neuronal Multicapa (MLP):
        - Capa de Entrada: 4 sensores (dist_jugador, bala_x, bala_y, dist_borde)
        - Capa Oculta: 4 Neuronas procesadoras
        - Capa de Salida: 1 Nodo de decisión (Movimiento horizontal)
        """
        # 1. Pesos de Capa de Entrada a Capa Oculta (Matriz 4x4)
        if pesos_entrada_oculta is not None:
            self.pesos_entrada_oculta = pesos_entrada_oculta
            self.bias_oculto = bias_oculto
        else:
            self.pesos_entrada_oculta = {
                f"n{j}": {
                    "w_dist_jugador": random.uniform(-1.0, 1.0),
                    "w_bala_x": random.uniform(-1.0, 1.0),
                    "w_bala_y": random.uniform(-1.0, 1.0),
                    "w_dist_borde": random.uniform(-1.0, 1.0),
                }
                for j in range(4)  # 4 neuronas ocultas (n0, n1, n2, n3)
            }
            self.bias_oculto = {f"b{j}": random.uniform(-0.5, 0.5) for j in range(4)}

        # 2. Pesos de Capa Oculta a Capa de Salida (Vector de 4 elementos + 1 Bias)
        self.pesos_oculta_salida = (
            pesos_oculta_salida
            if pesos_oculta_salida is not None
            else {f"w_n{j}": random.uniform(-1.0, 1.0) for j in range(4)}
        )
        self.bias_salida = (
            bias_salida if bias_salida is not None else random.uniform(-0.5, 0.5)
        )

        self.fitness = 0

    def procesar_decision(self, dist_jugador, bala_x, bala_y, dist_borde):
        """
        Procesamiento Forward Propagation (Paso hacia adelante):
        Mapea 4 entradas hacia 4 neuronas ocultas y reduce a 1 salida usando Tanh.
        """
        # Diccionario de entradas para facilitar el bucle interno
        entradas = {
            "w_dist_jugador": dist_jugador,
            "w_bala_x": bala_x,
            "w_bala_y": bala_y,
            "w_dist_borde": dist_borde,
        }

        # --- PASO 1: Calcular la activación de las 4 neuronas ocultas ---
        activaciones_ocultas = {}
        for j in range(4):
            id_nodo = f"n{j}"
            # Sumatoria lineal: Sum(X_i * W_ij) + Bias_j
            suma = sum(
                entradas[clave] * self.pesos_entrada_oculta[id_nodo][clave]
                for clave in entradas
            )
            suma += self.bias_oculto[f"b{j}"] # pyright: ignore[reportOptionalSubscript]
            # Función de activación no-lineal (Tangente Hiperbólica)
            activaciones_ocultas[id_nodo] = math.tanh(suma)

        # --- PASO 2: Calcular el output final combinando la capa oculta ---
        suma_salida = sum(
            activaciones_ocultas[f"n{j}"] * self.pesos_oculta_salida[f"w_n{j}"]
            for j in range(4)
        )
        suma_salida += self.bias_salida
        output_final = math.tanh(suma_salida)

        # --- PASO 3: Mapeo discreto de la acción de movimiento ---
        if output_final < -0.3:
            return -1  # Izquierda
        elif output_final > 0.3:
            return 1  # Derecha
        else:
            return 0  # Inmóvil/Quieto

    def clonar_con_mutacion(self, tasa_mutacion=0.15):
        """Aplica mutaciones gaussianas independientes a cada peso de la red matricial"""

        def mutar_valor(valor):
            if random.random() < tasa_mutacion:
                # Modificación incremental leve para preservar el conocimiento previo
                return valor + random.uniform(-0.3, 0.3)
            return valor

        # Mutar pesos entrada -> oculta
        nuevos_pesos_eo = {}
        nuevos_bias_o = {}
        for nodo, mapeo_pesos in self.pesos_entrada_oculta.items():
            nuevos_pesos_eo[nodo] = {
                clave: mutar_valor(val) for clave, val in mapeo_pesos.items()
            }
        for b_id, val in self.bias_oculto.items(): # pyright: ignore[reportOptionalMemberAccess]
            nuevos_bias_o[b_id] = mutar_valor(val)

        # Mutar pesos oculta -> salida
        nuevos_pesos_os = {
            clave: mutar_valor(val) for clave, val in self.pesos_oculta_salida.items()
        }
        nuevo_bias_s = mutar_valor(self.bias_salida)

        # Instanciar el hijo con la mutación completada
        hijo = CerebroAlien(
            nuevos_pesos_eo, nuevos_bias_o, nuevos_pesos_os, nuevo_bias_s
        )
        return hijo

    # --- SERIALIZACIÓN AVANZADA COMPATIBLE CON JSON ---
    def serializar(self):
        """Convierte la red multicapa estructurada en un formato JSON plano"""
        return {
            "fitness": int(self.fitness),
            "pesos": {
                "pesos_entrada_oculta": self.pesos_entrada_oculta,
                "bias_oculto": self.bias_oculto,
                "pesos_oculta_salida": self.pesos_oculta_salida,
                "bias_salida": self.bias_salida,
            },
        }

    @classmethod
    def deserializar(cls, datos):
        """Reconstruye de forma exacta las matrices y sesgos desde el diccionario JSON"""
        p = datos["pesos"]
        nuevo_cerebro = cls(
            pesos_entrada_oculta=p["pesos_entrada_oculta"],
            bias_oculto=p["bias_oculto"],
            pesos_oculta_salida=p["pesos_oculta_salida"],
            bias_salida=p["bias_salida"],
        )
        nuevo_cerebro.fitness = datos["fitness"]
        return nuevo_cerebro
