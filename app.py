from collections import Counter
from datetime import datetime
import os
import re
import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Contador e Ranking de Palavras", page_icon="📊", layout="centered"
)

ARQUIVO_HISTORICO = "historico.txt"


# Funções de persistência em arquivo
def carregar_historico():
  if os.path.exists(ARQUIVO_HISTORICO):
    with open(ARQUIVO_HISTORICO, "r", encoding="utf-8") as f:
      linhas = f.readlines()
    historico = []
    for linha in linhas:
      partes = linha.strip().split(" | ")
      if len(partes) == 2:
        historico.append({"data": partes[0], "conteudo": partes[1]})
    return historico
  return []


def salvar_no_historico(conteudo):
  agora = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
  with open(ARQUIVO_HISTORICO, "a", encoding="utf-8") as f:
    f.write(f"{agora} | {conteudo}\n")


def limpar_historico():
  if os.path.exists(ARQUIVO_HISTORICO):
    os.remove(ARQUIVO_HISTORICO)


# Função de autenticação simples
def verificar_senha():
  def senha_correta():
    if st.session_state["senha"] == "S3nh@SECRETA":  # Mude sua senha aqui!
      st.session_state["senha_correta"] = True
      del st.session_state["senha"]
    else:
      st.session_state["senha_correta"] = False

  if "senha_correta" not in st.session_state:
    st.text_input(
        "Digite sua senha de acesso:",
        type="password",
        on_change=senha_correta,
        key="senha",
    )
    return False
  elif not st.session_state["senha_correta"]:
    st.text_input(
        "Senha incorreta. Tente novamente:",
        type="password",
        on_change=senha_correta,
        key="senha",
    )
    st.error("Senha incorreta!")
    return False
  else:
    return True


if not verificar_senha():
  st.stop()

st.title("📊 Contador e Ranking Geral de Textos")
st.write(
    "Insira um novo texto abaixo. Ele será somado ao histórico acumulado e"
    " atualizará os rankings gerais."
)

# Caixa de texto para o usuário colar o conteúdo
texto_usuario = st.text_area(
    "Cole seu texto ou frases aqui:", height=150, placeholder="Digite ou cole aqui..."
)

if texto_usuario:
  historico_atual = carregar_historico()
  ultimo_registro = historico_atual[-1]["conteudo"] if historico_atual else ""

  # Salva automaticamente se for um texto novo
  if texto_usuario.strip() != ultimo_registro:
    salvar_no_historico(texto_usuario.strip())

# --- PROCESSAMENTO GLOBAL DO HISTÓRICO ---
historico_completo = carregar_historico()

# Junta o conteúdo de todas as entradas já salvas em um único texto gigante
texto_geral = " ".join([item["conteudo"] for item in historico_completo])

if texto_geral:
  # 1. Separa todas as frases de todo o histórico
  frases_brutas = re.split(r"[.!?\n]+", texto_geral)
  frases = [f.strip().lower() for f in frases_brutas if f.strip()]

  # 2. Extrai todas as palavras de todo o histórico
  texto_lower = texto_geral.lower()
  palavras = re.findall(r"\b\w+\b", texto_lower)

  # Gera os rankings acumulados
  ranking_frases = Counter(frases).most_common()
  ranking_palavras = Counter(palavras).most_common()

  # Abas na tela
  aba1, aba2, aba3, aba4 = st.tabs(
      [
          "📝 Ranking Geral de Frases",
          "🔤 Ranking Geral de Palavras",
          "🔍 Mecanismo de Busca Global",
          "📜 Histórico de Entradas",
      ]
  )

  with aba1:
    st.subheader("Ranking de Frases (Acumulado de Todo o Histórico)")
    for i, (frase, freq) in enumerate(ranking_frases, 1):
      st.markdown(f"**{i}.** \"{frase}\" — *({freq}x)*")

  with aba2:
    st.subheader("Ranking de Palavras Isoladas (Acumulado)")
    for i, (palavra, freq) in enumerate(ranking_palavras, 1):
      st.markdown(f"**{i}.** `{palavra}`: **{freq}x**")

  with aba3:
    st.subheader("Buscar Termo no Histórico Geral")
    termo_busca = st.text_input(
        "Digite a palavra ou frase que deseja procurar nos registros:"
    )

    if termo_busca:
      termo = termo_busca.strip().lower()
      dici_p = dict(ranking_palavras)
      dici_f = dict(ranking_frases)

      encontrou = False

      if termo in dici_p:
        pos_p = [p[0] for p in ranking_palavras].index(termo) + 1
        st.success(
            f"🔤 **[Palavra Isolada]** '{termo}' aparece **{dici_p[termo]}x**"
            f" no total acumulado (Posição: #{pos_p})"
        )
        encontrou = True

      if termo in dici_f:
        pos_f = [f[0] for f in ranking_frases].index(termo) + 1
        st.success(
            f"📝 **[Frase Completa]** '{termo}' aparece **{dici_f[termo]}x**"
            f" no total acumulado (Posição: #{pos_f})"
        )
        encontrou = True

      if not encontrou:
        st.error(
            f"❌ O termo '{termo}' não foi encontrado no histórico acumulado."
        )

  with aba4:
    st.subheader("📜 Histórico de Entradas Salvas")

    if historico_completo:
      if st.button("🗑️ Limpar Todo o Histórico"):
        limpar_historico()
        st.rerun()

      for item in reversed(historico_completo):
        st.markdown(f"🕒 **{item['data']}**")
        st.info(item["conteudo"])
        st.divider()
    else:
      st.info("Nenhuma entrada salva ainda.")
else:
  st.info("Insira um texto acima para começar a popular o histórico e os rankings.")
