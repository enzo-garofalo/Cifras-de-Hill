from flask import Flask, render_template, request, redirect, url_for
import numpy as np

alfabeto = {' ': 0,'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10, 'K': 11, 'L': 12, 'M': 13, 'N': 14, 'O': 15, 'P': 16, 'Q': 17, 'R': 18, 'S': 19, 'T': 20, 'U': 21, 'V': 22, 'W': 23, 'X': 24, 'Y': 25, 'Z': 26}

def criptografar(palavra):
  palavra = palavra.upper()
  matriz_palavra_em_num = np.array([[], []])

  palavra_impar = False
  if len(palavra) % 2 != 0:
      palavra += "A"
      palavra_impar = True

  matriz_palavra_em_num = palavra_em_matriz(palavra)
  chaveMatriz = np.array([[4, 3], [1, 2]])
  criptografada = np.dot(chaveMatriz, matriz_palavra_em_num) % 26
  return monta_palavra(criptografada, palavra_impar)

def decifrar(palavra):
  palavra_criptograda = palavra.upper()
  matriz_palavra_em_num = palavra_em_matriz(palavra_criptograda)
  a = 4
  b = 3
  c = 1
  d = 2
  chaveMatrizInversa = np.array([[d, -b], [-c, a]])
  det = (a*d)-(c*b)
  det_inversas = {1: 1, 3: 9, 5: 21, 7: 15, 9: 3, 11: 19, 15: 7, 17: 23, 19: 11, 21: 5, 23: 17, 25: 25}
  for chave, valor in det_inversas.items():
     if det == chave:
        det = valor
        break
  chaveMatrizInversa *= det
  matriz_palavra_em_num = np.dot(chaveMatrizInversa, matriz_palavra_em_num)%26
  return monta_palavra(matriz_palavra_em_num, False)

def palavra_em_matriz(palavra):
  letras = []
  matriz_palavra_em_num = np.array([[], []])
  for letra in range(len(palavra)):
    for chave, valor in alfabeto.items():
      if palavra[letra] == chave:
          letras.append(valor)
  for i in range(0, len(palavra)-1, 2):  
      novaColuna = np.array([[letras[i]], [letras[i+1]]])
      matriz_palavra_em_num = np.append(matriz_palavra_em_num, novaColuna, axis=1)
  return matriz_palavra_em_num

def monta_palavra(matriz, palavra_impar):
  palavra_formada = ''
  for linha in matriz.T:
      for num in linha:
          if num == 0:  
              palavra_formada += 'Z'
          else:
              for chave, valor in alfabeto.items():
                  if num == valor:
                      palavra_formada += chave
  if palavra_impar is True:
    palavra_formada = palavra_formada[:-1]
  return palavra_formada

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html', title='Hill Cipher')

@app.route('/calcular', methods=['POST',])
def calcular():
  palavra = request.form['palavra']
  choice = request.form['choice']

  if choice == 'decifrar':
    resposta = decifrar(palavra)
  else:
    resposta = criptografar(palavra)

  return redirect(url_for('responder', resposta=resposta))

@app.route('/responder/<resposta>')
def responder(resposta):
    return render_template('responder.html', resposta=resposta)

if __name__ == '__main__':
  app.run(debug=True)