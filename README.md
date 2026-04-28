# scalable_supply_chain_analytics_pipeline
Producto analítico para retail y supply chain que integra ventas, inventario y movimientos en un modelo escalable para análisis, basado en arquitectura Medallion

# Scalable Supply Chain Analytics Pipeline

## Overview
This project builds an end-to-end data pipeline for retail supply chain analytics using Medallion Architecture (Bronze → Silver → Gold).

## Features
- Sales analytics
- Inventory tracking
- Movement analysis
- Power BI ready dataset

## Insights
![insights](insights.png)



 ### cuando los datos no dicen nada…
Todo empezó con algo bastante común, muchos datos, pero poca claridad.
Ventas por un lado, inventario por otro, movimientos por otro… todo existía, pero no estaba conectado.

Y ahí es donde aparece el problema real:
👉 no puedes tomar decisiones si no ves la historia completa.

La idea de este proyecto fue simple:
convertir datos dispersos en una visión clara del negocio.

🔍 Exploración, entender qué está pasando realmente
Antes de construir nada, había que entender los datos.

¿Qué se estaba vendiendo?

Aquí fue clave organizar todo en capas (tipo Bronze → Silver → Gold), no por moda, sino porque:
👉 te obliga a estructurar y confiar en lo que estás viendo.

Fue como pasar de tener piezas sueltas… a empezar a ver el rompecabezas.

 #### ⚙️ Proceso, conectar todo (de verdad)
La parte más interesante fue unir tres mundos que normalmente viven separados:

📦 Inventario (lo que tienes)

💰 Ventas (lo que sale)

🔄 Movimientos (cómo se mueve)

Al combinarlos semana a semana, por producto y ubicación, empezó a aparecer algo poderoso:

👉 una visión completa del comportamiento del negocio

Ya no era solo “vendí mucho”
Ahora era:

vendí mucho pero me quedé sin stock

tengo mucho inventario pero no se vende

se mueve stock pero no impacta ventas

Ahí es donde los datos dejan de ser números… y empiezan a contar historias.

 #### 📊 Resultados: de datos a decisiones
Con todo estructurado, el dashboard cobra sentido.

Se pueden ver cosas como:

ventas vs inventario disponible

productos con riesgo de quiebre de stock

exceso de inventario

comportamiento por región o categoría

Y lo más importante:
👉 todo está conectado en una sola vista

Esto permite responder preguntas reales del negocio, como:


¿Qué productos necesitan mejor reposición?

 #### 💭 Cierre lo que realmente importa
Este proyecto no trata de DuckDB, ni de Power BI, ni de scripts…

Trata de esto,
👉 hacer que los datos sirvan para tomar decisiones reales

La mayor lección fue entender que:

un dashboard bonito no sirve si no conecta con decisiones

los datos aislados no generan valor

la claridad es más importante que la complejidad

Al final, construir esto fue pasar de:
📉 datos sueltos
a
📈 una historia clara del negocio

Y eso… es lo que realmente hace útil a la analítica.
