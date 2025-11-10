from datetime import datetime, time
import re

def validar_email(email: str) -> bool:
    """Valida formato de email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validar_horario_comercial(inicio: datetime, fim: datetime) -> bool:
    """
    Valida se o horário está dentro do período comercial
    (8h às 18h, por exemplo)
    """
    hora_inicio = inicio.time()
    hora_fim = fim.time()
    
    horario_abertura = time(8, 0)   # 8:00 AM
    horario_fechamento = time(18, 0) # 6:00 PM
    
    return (hora_inicio >= horario_abertura and 
            hora_fim <= horario_fechamento and
            hora_inicio < hora_fim)

def calcular_duracao_horas(inicio: datetime, fim: datetime) -> float:
    """Calcula duração em horas entre duas datas"""
    return (fim - inicio).total_seconds() / 3600

def validar_duracao_minima(inicio: datetime, fim: datetime, duracao_minima_horas: float = 1.0) -> bool:
    """Valida duração mínima da reserva"""
    duracao = calcular_duracao_horas(inicio, fim)
    return duracao >= duracao_minima_horas

def validar_antecedencia_minima(inicio: datetime, horas_antecedencia: int = 2) -> bool:
    """Valida antecedência mínima para reserva"""
    agora = datetime.now()
    diferenca_horas = (inicio - agora).total_seconds() / 3600
    return diferenca_horas >= horas_antecedencia