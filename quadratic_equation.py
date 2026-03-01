import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from mpl_toolkits.mplot3d import Axes3D

def quadraticEqGenerator(nSamples):
  '''   Funkcja generuje nSamples losowych wartości współczynników równania i zwraca wynik w postaci macierzy numpy o kształcie (nSamples, 3).  '''
  wspolczynniki = np.random.default_rng(42).uniform(-1., 1., (nSamples,3))
  return wspolczynniki

def quadraticEqSolution(coeff):
  ''' 
  Funkcja bierze macierz o kształcie (n,3), gdzie kolumny to współczynniki równania: a,b,c, a wiersze to kolejne równania. 
  Funkcja zwraca krotkę macierz o kształcie (n, 2), gdzie dwie kolumny to (x1,x2) jeśli równanie ma rozwiązania, lub None jeśli nie ma rozwiązań.
  Jeśli równanie ma jedno rozwiązanie należy umieścić je w obu polach krotki 
  '''
  coeff = np.asarray(coeff)
  n = coeff.shape[0]

  a = coeff[:, 0]
  b = coeff[:, 1]
  c = coeff[:, 2]
  
  result = np.empty((n, 2), dtype='d')
  delta = b**2 - 4*a*c

  for i in range(n):
    if delta[i] > 0:
      x1 = (-b[i] + np.sqrt(delta[i]))/(2*a[i])
      x2 = (-b[i] - np.sqrt(delta[i]))/(2*a[i])
      result[i] = (x1, x2)
    elif delta[i] == 0:
      x1 = -b[i]/(2*a[i])
      result[i] = (x1, x1)
    else: 
      result[i] = (None, None)

  return result

def plotQuadraticEqSolvability(z, interactive=False):
  ''' Funkcja rysuje współczynniki równania kwadratowego w przestrzeni 3D. 
  Współczynniki dla których równanie ma rozwiązania powinny być oznaczone innym kolorem niż pozostałe współczynniki '''
  z = np.asarray(z)

  a = z[:, 0]
  b = z[:, 1]
  c = z[:, 2]

  delta = b**2 - 4*a*c
  solvable = delta >= 0

  if interactive:
    try:
      colors = np.where(solvable, 'Ma rozwiązaznia rzeczywiste.', 'Nie ma rozwiązań rzeczywistych.')
      fig = px.scatter_3d(x=a, y=b, z=c, color=colors, hover_name=colors, labels=dict(x="a", y="b", z="c"), title="Rozwiązywalność równania kwadratowego.")
      fig.show()
    except ImportError:
      print("Plotly nie jest zainstalowany. Używam matplotlib.")
      interactive = False

  if not interactive:
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(a[solvable], b[solvable], c[solvable], c='r', marker='o', label='Rozwiązania rzeczywiste')
    ax.scatter(a[~solvable], b[~solvable], c[~solvable], c='b', marker='o', label='Brak rozwiązań rzeczywistych')
    ax.set_xlabel('a')
    ax.set_ylabel('b')
    ax.set_zlabel('c')
    ax.legend()
    plt.title("Rozwiązywalność równania kwadratowego.")
    plt.tight_layout()
    plt.show()
