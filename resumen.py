"""
Generador de Resumen Ejecutivo en PDF
======================================
Crea un documento PDF profesional del proyecto
"""

from reportlab.lib.pagesizes import A4, letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime

def crear_resumen_ejecutivo():
    """Crea el PDF del resumen ejecutivo"""
    
    # Crear documento
    filename = "Resumen_Ejecutivo_Simulacion_Resonador.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter,
                           topMargin=0.75*inch, bottomMargin=0.75*inch,
                           leftMargin=0.75*inch, rightMargin=0.75*inch)
    
    # Estilos
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a5490'),
        spaceAfter=30,
        alignment=1  # Center
    ))
    styles.add(ParagraphStyle(
        name='SectionHeader',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#1a5490'),
        spaceAfter=12,
        spaceBefore=12
    ))
    
    # Contenido
    story = []
    
    # ========================================================================
    # PORTADA
    # ========================================================================
    story.append(Spacer(1, 1.5*inch))
    
    title = Paragraph("SIMULACIÓN DE RESONADOR", styles['CustomTitle'])
    story.append(title)
    story.append(Spacer(1, 0.1*inch))
    
    subtitle = Paragraph("Análisis y Optimización del Flujo de Pacientes", 
                        ParagraphStyle('subtitle', parent=styles['Heading3'], 
                                     fontSize=14, alignment=1))
    story.append(subtitle)
    story.append(Spacer(1, 0.5*inch))
    
    # Línea divisoria
    story.append(Spacer(1, 0.3*inch))
    
    # Info del documento
    info = Paragraph(f"<b>Fecha:</b> {datetime.now().strftime('%d de %B de %Y')}<br/>"
                    f"<b>Versión:</b> 1.0<br/>"
                    f"<b>Tipo:</b> Resumen Ejecutivo",
                    styles['Normal'])
    story.append(info)
    
    story.append(PageBreak())
    
    # ========================================================================
    # RESUMEN EJECUTIVO
    # ========================================================================
    story.append(Paragraph("RESUMEN EJECUTIVO", styles['SectionHeader']))
    
    texto_resumen = """
    Este proyecto implementa una <b>simulación avanzada del flujo de pacientes</b> 
    en el servicio de resonancia magnética de la clínica, utilizando técnicas de 
    <b>simulación de eventos discretos</b> y <b>análisis estadístico de Monte Carlo</b>.
    <br/><br/>
    La simulación permite visualizar en tiempo real el recorrido completo de cada 
    paciente, desde su llegada hasta la finalización del estudio, midiendo métricas 
    clave para optimizar la operación del servicio.
    """
    story.append(Paragraph(texto_resumen, styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # ========================================================================
    # OBJETIVOS
    # ========================================================================
    story.append(Paragraph("OBJETIVOS DEL PROYECTO", styles['SectionHeader']))
    
    objetivos = [
        "Modelar el flujo completo de pacientes con precisión estadística",
        "Identificar cuellos de botella y tiempos de espera innecesarios",
        "Optimizar la asignación de turnos para maximizar la utilización del resonador",
        "Reducir el tiempo ocioso del equipo y mejorar la rentabilidad",
        "Proporcionar datos cuantitativos para la toma de decisiones estratégicas"
    ]
    
    for i, objetivo in enumerate(objetivos, 1):
        story.append(Paragraph(f"{i}. {objetivo}", styles['Normal']))
        story.append(Spacer(1, 0.1*inch))
    
    story.append(Spacer(1, 0.3*inch))
    
    # ========================================================================
    # METODOLOGÍA
    # ========================================================================
    story.append(Paragraph("METODOLOGÍA", styles['SectionHeader']))
    
    texto_metodologia = """
    <b>1. Simulación de Monte Carlo</b><br/>
    Se iteraron 10,000 escenarios para obtener distribuciones probabilísticas 
    realistas de todos los tiempos y eventos del sistema.
    <br/><br/>
    <b>2. Eventos Discretos</b><br/>
    Cada paciente es modelado como una entidad independiente que transita por 
    diferentes estados y recursos (mesa de atención, cambiador, resonador).
    <br/><br/>
    <b>3. Distribuciones Estadísticas</b><br/>
    Se utilizan distribuciones normales para tiempos de servicio y distribuciones 
    discretas para tipos de estudios, basadas en datos históricos reales.
    """
    story.append(Paragraph(texto_metodologia, styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # ========================================================================
    # MÉTRICAS CLAVE
    # ========================================================================
    story.append(Paragraph("MÉTRICAS MEDIDAS", styles['SectionHeader']))
    
    # Tabla de métricas por paciente
    data_metricas_paciente = [
        ['Métrica', 'Descripción'],
        ['Tiempo de llegada', 'Desviación del turno asignado (temprano/tarde)'],
        ['Tiempo de validación', 'Duración en mesa de atención'],
        ['Tiempo en cambiador', 'Entrada y salida del vestuario'],
        ['Tiempo de scan', 'Duración del estudio por tipo'],
        ['Tiempo total', 'Desde llegada hasta salida completa']
    ]
    
    tabla_paciente = Table(data_metricas_paciente, colWidths=[2*inch, 4*inch])
    tabla_paciente.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5490')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9)
    ]))
    
    story.append(Paragraph("<b>Métricas por Paciente:</b>", styles['Normal']))
    story.append(Spacer(1, 0.1*inch))
    story.append(tabla_paciente)
    story.append(Spacer(1, 0.3*inch))
    
    # Tabla de métricas globales
    data_metricas_globales = [
        ['Métrica', 'Descripción'],
        ['Utilización del resonador', 'Porcentaje de tiempo ocupado vs. ocioso'],
        ['Tiempo de espera promedio', 'Tiempo perdido en colas'],
        ['Pacientes atendidos/día', 'Throughput del sistema'],
        ['Eficiencia de turnos', 'Adherencia al horario programado']
    ]
    
    tabla_global = Table(data_metricas_globales, colWidths=[2*inch, 4*inch])
    tabla_global.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5490')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9)
    ]))
    
    story.append(Paragraph("<b>Métricas Globales del Sistema:</b>", styles['Normal']))
    story.append(Spacer(1, 0.1*inch))
    story.append(tabla_global)
    
    story.append(PageBreak())
    
    # ========================================================================
    # PARÁMETROS ESTADÍSTICOS
    # ========================================================================
    story.append(Paragraph("PARÁMETROS ESTADÍSTICOS", styles['SectionHeader']))
    
    # Tabla de tipos de estudios
    data_estudios = [
        ['Tipo de Estudio', 'Duración (min)', 'Probabilidad'],
        ['RMN de Cerebro', '4.45', '25%'],
        ['RMN de Columna', '5.20', '25%'],
        ['RMN de Articulaciones', '4.53', '33%'],
        ['RMN de Cuerpo Completo', '20.00', '2%'],
        ['Otros Estudios', '5.00', '15%']
    ]
    
    tabla_estudios = Table(data_estudios, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
    tabla_estudios.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5490')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9)
    ]))
    
    story.append(Paragraph("<b>Distribución de Tipos de Estudios:</b>", styles['Normal']))
    story.append(Spacer(1, 0.1*inch))
    story.append(tabla_estudios)
    story.append(Spacer(1, 0.3*inch))
    
    # Distribuciones normales
    data_dist = [
        ['Proceso', 'Media (μ)', 'Desv. Est. (σ)'],
        ['Validación administrativa', '5 min', '1 min'],
        ['Cambiador (entrada)', '6 min', '1.5 min'],
        ['Posicionamiento en resonador', '3 min', '0.5 min'],
        ['Cambiador (salida)', '4 min', '1 min']
    ]
    
    tabla_dist = Table(data_dist, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
    tabla_dist.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5490')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9)
    ]))
    
    story.append(Paragraph("<b>Distribuciones Normales de Tiempos:</b>", styles['Normal']))
    story.append(Spacer(1, 0.1*inch))
    story.append(tabla_dist)
    story.append(Spacer(1, 0.3*inch))
    
    # ========================================================================
    # CARACTERÍSTICAS TÉCNICAS
    # ========================================================================
    story.append(Paragraph("CARACTERÍSTICAS TÉCNICAS", styles['SectionHeader']))
    
    caracteristicas = [
        "<b>Visualización 2D interactiva</b>: Interfaz gráfica que muestra el plano de la clínica y el movimiento de pacientes en tiempo real",
        "<b>Panel de métricas en vivo</b>: Monitoreo constante de utilización del resonador y tiempos de espera",
        "<b>Control de velocidad</b>: Ajuste dinámico de la velocidad de simulación (1x a 960x)",
        "<b>Código modular</b>: Arquitectura escalable para futuras mejoras",
        "<b>Exportación de datos</b>: Métricas exportables para análisis posterior"
    ]
    
    for carac in caracteristicas:
        story.append(Paragraph(f"• {carac}", styles['Normal']))
        story.append(Spacer(1, 0.08*inch))
    
    story.append(PageBreak())
    
    # ========================================================================
    # RESULTADOS ESPERADOS
    # ========================================================================
    story.append(Paragraph("RESULTADOS ESPERADOS", styles['SectionHeader']))
    
    texto_resultados = """
    <b>Optimización de Turnos:</b><br/>
    Reducción del tiempo ocioso del resonador mediante asignación dinámica de turnos 
    basada en duración real de estudios.<br/><br/>
    
    <b>Mejora en la Experiencia del Paciente:</b><br/>
    Minimización de tiempos de espera innecesarios y mejor predicción de tiempos 
    de atención.<br/><br/>
    
    <b>Aumento de Rentabilidad:</b><br/>
    Mayor cantidad de estudios por día sin comprometer la calidad del servicio.<br/><br/>
    
    <b>Toma de Decisiones Basada en Datos:</b><br/>
    Métricas cuantitativas para evaluar cambios operacionales antes de implementarlos.
    """
    story.append(Paragraph(texto_resultados, styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # ========================================================================
    # PRÓXIMOS PASOS
    # ========================================================================
    story.append(Paragraph("PRÓXIMOS PASOS", styles['SectionHeader']))
    
    proximos_pasos = [
        "<b>Fase 1 (Actual):</b> Validación del modelo 2D con datos reales de la clínica",
        "<b>Fase 2:</b> Implementación de diferentes escenarios de optimización",
        "<b>Fase 3:</b> Desarrollo de visualización 3D inmersiva",
        "<b>Fase 4:</b> Dashboard web para acceso remoto de directivos",
        "<b>Fase 5:</b> Sistema de predicción y alertas en tiempo real"
    ]
    
    for paso in proximos_pasos:
        story.append(Paragraph(f"• {paso}", styles['Normal']))
        story.append(Spacer(1, 0.12*inch))
    
    story.append(Spacer(1, 0.4*inch))
    
    # ========================================================================
    # CONCLUSIÓN
    # ========================================================================
    story.append(Paragraph("CONCLUSIÓN", styles['SectionHeader']))
    
    texto_conclusion = """
    Este proyecto representa una <b>herramienta innovadora</b> para la gestión 
    y optimización del servicio de resonancia magnética. La combinación de análisis 
    estadístico riguroso con visualización interactiva permite tomar decisiones 
    informadas para mejorar tanto la eficiencia operativa como la satisfacción 
    del paciente.
    <br/><br/>
    La inversión en esta simulación se traducirá en <b>retornos medibles</b> 
    mediante el aumento de la utilización del equipo y la reducción de costos 
    operativos por capacidad ociosa.
    """
    story.append(Paragraph(texto_conclusion, styles['Normal']))
    
    # Generar PDF
    doc.build(story)
    print(f"\n✅ PDF generado exitosamente: {filename}")
    return filename

if __name__ == "__main__":
    print("=" * 60)
    print("GENERADOR DE RESUMEN EJECUTIVO")
    print("=" * 60)
    crear_resumen_ejecutivo()
    print("=" * 60)
