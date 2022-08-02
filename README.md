# Clasificador-noticias

Este proyecto intenta simular un clasificador de noticias basado en el modelo probabilístico <i>Naïve-Bayes</i>: dado un artículo o el vector de características que lo describe, se indicará la categoría o tópico al que tiene más probabilidad de pertenecer.

### Datos

Los datos corresponden a cada uno de los titulares de la primera plana del <i>New Your Times</i> entre 1996 y 2006, clasificados según <i>Policy Agendas</i> (http://www.policyagendas.org) y recogidos y compilados por <i>Amber E. Boydstun</i>. En total se tienen los 27 tópicos siguientes:

<table border="1">
  <tr><td>1<td>Macroeconomics
  <tr><td>2<td>Civil Rights, Minority Issues, and Civil Liberties
  <tr><td>3<td>Health
  <tr><td>4<td>Agriculture
  <tr><td>5<td>Labor, Employment, and Immigration
  <tr><td>6<td>Education
  <tr><td>7<td>Environment
  <tr><td>8<td>Energy
  <tr><td>10<td>Transportation
  <tr><td>12<td>Law, Crime, and Family Issues
  <tr><td>13<td>Social Welfare
  <tr><td>14<td>Community Development and Housing Issues
  <tr><td>15<td>Banking, Finance, and Domestic Commerce
  <tr><td>16<td>Defense
  <tr><td>17<td>Space, Science, Technology and Communications
  <tr><td>18<td>Foreign Trade
  <tr><td>19<td>International Affairs and Foreign Aid
  <tr><td>20<td>Government Operations
  <tr><td>21<td>Public Lands and Water Management
  <tr><td>24<td>State and Local Government Administration
  <tr><td>26<td>Weather and Natural Disasters
  <tr><td>27<td>Fires
  <tr><td>28<td>Arts and Entertainment
  <tr><td>29<td>Sports and Recreation
  <tr><td>30<td>Death Notices
  <tr><td>31<td>Churches and Religion
  <tr><td>99<td>Other, Miscellaneous, and Human Interest
</table>

### Vector de características

Al trabajar con lenguaje natural, para la construcción del vector de características se usará el modelo <i>bag-of-words</i>, en el que un documento de texto se representa como un conjunto de palabras. Así, seleccionando las N palabras más representativas de cada uno de los tópicos y tomando la unión de todas ellas sin repetición (<i>p<sub>1</sub>,...,p<sub>n</sub></i>), definiremos el vector de características de un artículo como un vector booleano <i>(v<sub>1</sub>,...,v<sub>n</sub>)</i> dónde:
<ul>
  <li><i>v<sub>i</sub> = True</i> si <i>p<sub>i</sub></i> aparece en el artículo</li>
  <li><i>v<sub>i</sub> = False</i> si <i>p<sub>i</sub></i> no aparece en el artículo</li>
</ul>

### Cálculo de probabilidad

Los clasificadores probabilísticos Bayesianos se basan en el teorema de Bayes para calcular la probabilidad condicionada:

$$ p(x,y) = p(x|y)p(y) = p(y|x)p(x) $$

de dónde se extrae que:

$$ p(y|x) = \frac{p(x|y)p(y)}{p(x)} $$

En muchos casos <i>p(y)</i> y <i>p(x)</i> son desconocidos y se consideran equiprobables, por lo que la ecuación se simplifica a:

$$ p(y|x) = c · p(x|y)$$

El método <i>Naïve-Bayes</i> va más allá de los clasificadores Bayesianos y asume que las variables aleatorias <i>x = (x<sub>1</sub>,...,x<sub>n</sub>)</i> son independientes entre ellas y, por lo tanto, se tiene que:

$$ p (x|y) = p(x<sub>1</sub>,...,x<sub>n</sub> | y) = p(x<sub>1</sub>|y)...p(x<sub>n</sub>|y) $$

En nuestro caso:
<ul>
  <li><i>'x'</i> corresponde al vector de características asociado al artículo que queremos clasificar</li>
  <li><i>'y'</i> corresponde al tópico para el que estamos calculando la probabilidad
</ul>
es decir, la probabilidad de que el artículo con vector de características <i>v = (v<sub>1</sub>,...,v<sub>n</sub>)</i> pertenezca a la categoría <i>'C'</i> es igual a:

$$ p(x=v|y=C) = p(x_1=v_1|y=C)p(x_2=v_2|y=C)...p(x_n=v_n|y=C) $$

dónde <i>p(x<sub>i</sub>=v<sub>i</sub>|y=C)</i>, aplicando la corrección de Laplace para evitar resultados con probabilidad cero, corresponde a:

$$ p(x_i=v_i|y=C) = \frac{A + 1}{B + M}$$

<ul>
  <li><i>'M'</i> es el número total de categorías</li>
  <li><i>'B'</i> es el número total de noticias de la categoría <i>'C'</i></li>
  <li><i>'A'</i> es el número de noticias de la categoría <i>'C'</i> en el que:
    <ul>
      <li><b>aparece</b> la palabra <i>x<sub>i</sub></i> si <i>v<sub>i</sub> = <b>True</b></i></li>
      <li><b>NO aparece</b> la palabra <i>x<sub>i</sub></i> si <i>v<sub>i</sub> = <b>False</b></i></li>
    </ul>
  </li>
</ul>

Como la probabilidad resultante es un producto de probabilidades, este valor podría resultar demasiado pequeño para ser representado por un punto flotante y acabar siendo reducido a cero. Para evitarlo, trabajaremos con logaritmos y sumaremos las probabilidades en vez de multiplicarlas.

### Validación

Para validar el clasificador se usará el método <i>n-fold cross-validation</i>, que consiste en dividir el conjunto de datos en <i>n</i> subconjuntos y realizar <i>n</i> iteraciones en las cuales para cada una de ellas se toma un subconjunto diferente como datos de test y el resto como datos de entrenamiento. El error final del clasificador vendrá dado por la media aritmética del error obtenido en cada una de las iteraciones.
