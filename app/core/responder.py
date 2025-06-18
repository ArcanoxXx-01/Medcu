class ResponderInterface:
    def generar_respuesta_error(self, mensaje: str) -> None:
        raise NotImplementedError

    def generar_respuesta_diagnostico(self, diagnostico: str, entidades: list[str]) -> None:
        raise NotImplementedError

    def preguntar_usuario(self, entidad: str) -> bool:
        raise NotImplementedError