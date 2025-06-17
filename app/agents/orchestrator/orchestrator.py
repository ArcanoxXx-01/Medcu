import random

class OrquestadorMedico:
    def __init__(self):
        self.diagnostic = "Perdón, aún no he sido capaz de generar un diagóstico."
        " Podrías volver a intentarlo explicando detalladamente los síntomas que presentas"

    def diagnose(self, 
            sintomas_presentes:         list[str], 
            enfermedades_presentes:     list[str], 
            sintomas_excluidos:         list[str] = [],
            enfermedades_excluidas:     list[str] = [],
            consulta_original:          str = "No hay consulta"
            ) -> str:
        """
        Genera un diagnóstico
        """
        pass
    
    
