from typing import Dict, Set, Tuple

class NFA:
    def __init__(self, states: Set[str], alphabet: Set[str],
                 transitions: Dict[Tuple[str, str], Set[str]],
                 start_state: str, accept_states: Set[str]):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions  # map (state, symbol) -> set(next_states)
        self.start_state = start_state
        self.accept_states = accept_states

    def step(self, current_states: Set[str], symbol: str) -> Set[str]:
        """Una sola transición consumiendo `symbol` desde el conjunto current_states."""
        next_states = set()
        for s in current_states:
            key = (s, symbol)
            if key in self.transitions:
                next_states |= self.transitions[key]
        return next_states

    def accepts(self, w: str, debug: bool = False) -> bool:
        """Simula el AFN (sin epsilon-closures porque no usamos epsilons aquí)."""
        # Validación rápida: símbolos fuera del alfabeto causan rechazo
        for ch in w:
            if not any(ch in group for group in [UPPER, LOWER, DIGITS]):
                # símbolo no permitido por la política
                if debug:
                    print(f"Carácter inválido detectado: '{ch}'")
                return False

        current = {self.start_state}
        if debug:
            print(f"entrada: '{w}'")
            print(f"estado inicial: {current}")

        for i, ch in enumerate(w):
            current = self.step(current, ch)
            if debug:
                print(f" tras consumir '{ch}' -> {current}")
            if not current:
                if debug:
                    print("No hay transiciones posibles, cadena rechazada.")
                return False

        accepted = any(s in self.accept_states for s in current)
        if debug:
            print("estados finales tras consumir toda la cadena:", current)
            print("aceptada?" , accepted)
        return accepted


# --- Definición del alfabeto (como conjuntos para comprobaciones) ---
UPPER = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
LOWER = set("abcdefghijklmnopqrstuvwxyz")
DIGITS = set("0123456789")
ALPHABET = UPPER | LOWER | DIGITS

# --- Estados ---
Q = {"q0", "q1", "q2", "q3"}  # nombres simbólicos

# --- Transiciones tal como se describieron arriba ---
# Representamos transiciones con claves (estado_origen, símbolo) -> {estados_destino}
transitions = {}

def add_transition(frm: str, symbol_set: Set[str], to: str):
    for sym in symbol_set:
        key = (frm, sym)
        transitions.setdefault(key, set()).add(to)

# δ(q0, A-Z) -> q1
add_transition("q0", UPPER, "q1")

# δ(q1, a-z) -> q2   (entra en minúsculas opcionales)
add_transition("q1", LOWER, "q2")
# δ(q1, 0-9) -> q3   (si después de la mayúscula vienen dígitos directamente)
add_transition("q1", DIGITS, "q3")

# δ(q2, a-z) -> q2   (loop de minúsculas)
add_transition("q2", LOWER, "q2")
# δ(q2, 0-9) -> q3   (transición a la zona de dígitos)
add_transition("q2", DIGITS, "q3")

# δ(q3, 0-9) -> q3   (al menos un dígito, loop en q3)
add_transition("q3", DIGITS, "q3")

# --- Construimos el NFA ---
nfa_password = NFA(states=Q, alphabet=ALPHABET,
                   transitions=transitions,
                   start_state="q0",
                   accept_states={"q3"})

# --- Cadenas de prueba proporcionadas en el enunciado ---
accepted_examples = ["A123", "Sogamoso2025", "Uptc9", "X0", "Z99"]
rejected_examples = ["1234", "soga2025", "UPTC", "aX99", "AA1"]

def run_tests(nfa: NFA):
    print("\n-- Pruebas con ejemplos del enunciado --")
    print("\nAceptadas (esperado: aceptadas):")
    for s in accepted_examples:
        result = nfa.accepts(s)
        print(f"  {s:15} -> {'ACEPTADA' if result else 'RECHAZADA'}")
    print("\nRechazadas (esperado: rechazadas):")
    for s in rejected_examples:
        result = nfa.accepts(s)
        print(f"  {s:15} -> {'ACEPTADA' if result else 'RECHAZADA'}")

if __name__ == "__main__":
    run_tests(nfa_password)

    # Ejemplo interactivo rápido:
    print("\nPrueba interactiva rápida. Introduce cadenas (enter vacío o 'salir' para terminar):")
    while True:
        try:
            s = input("cadena> ").strip()
        except EOFError:
            break
        if s == "" or s.lower() in ("salir", "exit"):
            print("👋 Programa finalizado por el usuario.")
            break
        ok = nfa_password.accepts(s, debug=True)
        print("→", "ACEPTADA" if ok else "RECHAZADA")
        print("-" * 30)
