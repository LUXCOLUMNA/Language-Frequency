from collections import Counter
import re
import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Contador e Ranking de Palavras", page_icon="📊", layout="centered"
)


# Função de autenticação simples
def verificar_senha():
  """Retorna True se o usuário digitou a senha correta."""

  def senha_correta():
    if st.session_state["senha"] == "S3nh@SECRETA":  # Mude a senha aqui!
      st.session_state["senha_correta"] = True
      del st.session_state["senha"]  # Remove a senha da memória por segurança
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


# Se a senha estiver incorreta, para a execução aqui
if not verificar_senha():
  st.stop()

# --- A PARTIR DAQUI É O SEU PROGRAMA (Área Protegida) ---

st.title("📊 Contador e Ranking de Textos")
st.write(
    "Cole seu texto abaixo para gerar o ranking de frases e palavras isoladas."
)

# Caixa de texto para o usuário colar o conteúdo
texto_usuario = st.text_area(
    "Cole seu texto ou frases aqui:", height=150, placeholder="Digite ou cole aqui..."
)

if texto_usuario:
  # 1. Separa o texto em frases
  frases_brutas = re.split(r"[.!?\n]+", texto_usuario)
  frases = [f.strip().lower() for f in frases_brutas if f.strip()]

  # 2. Extrai TODAS as palavras
  texto_lower = texto_usuario.lower()
  palavras = re.findall(r"\b\w+\b", texto_lower)

  # Gera os rankings
  ranking_frases = Counter(frases).most_common()
  ranking_palavras = Counter(palavras).most_common()

  # Abas na tela para separar Frases e Palavras
  aba1, aba2, aba3 = st.tabs(
      ["📝 Ranking de Frases", "🔤 Ranking de Palavras", "🔍 Mecanismo de Busca"]
  )

  with aba1:
    st.subheader("Ranking de Frases")
    for i, (frase, freq) in enumerate(ranking_frases, 1):
      st.markdown(f"**{i}.** \"{frase}\" — *({freq}x)*")

  with aba2:
    st.subheader("Ranking de Palavras Isoladas")
    for i, (palavra, freq) in enumerate(ranking_palavras, 1):
      st.markdown(f"**{i}.** `{palavra}`: **{freq}x**")

  with aba3:
    st.subheader("Buscar Termo")
    termo_busca = st.text_input("Digite a palavra ou frase que deseja procurar:")

    if termo_busca:
      termo = termo_busca.strip().lower()
      dici_p = dict(ranking_palavras)
      dici_f = dict(ranking_frases)

      encontrou = False

      if termo in dici_p:
        pos_p = [p[0] for p in ranking_palavras].index(termo) + 1
        st.success(
            f"🔤 **[Palavra Isolada]** '{termo}' aparece **{dici_p[termo]}x**"
            f" (Posição: #{pos_p})"
        )
        encontrou = True

      if termo in dici_f:
        pos_f = [f[0] for f in ranking_frases].index(termo) + 1
        st.success(
            f"📝 **[Frase Completa]** '{termo}' aparece **{dici_f[frase] if termo in dici_f else ''}x**"
            f" (Posição: #{pos_f})"
        )
        encontrou = True

      if not encontrou:
        st.error(
            f"❌ O termo '{termo}' não foi encontrado em nenhuma das"
            " categorias."
        )
