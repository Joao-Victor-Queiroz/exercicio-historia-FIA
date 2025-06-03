
import streamlit as st
import google.generativeai as genai

api_key = st.secrets("API_KEY")

genai.configure(api_key="AIzaSyADzjCSDDmcDAYzVJu01hHsUcClQR9pThE")


try:
    model =  genai.GenerativeModel("gemini-2.0-flash")
except Exception as e:
    st.error(f"Erro ao carregar o modelo Gemini 'gemini-2.0-flash': {e}")
    st.info("Verifique se o nome do modelo está correto e se sua chave API tem acesso a ele.")
    st.stop()


def gerar_resposta_gemini(prompt_completo):
    try:
        response = model.generate_content(prompt_completo)

        if response.parts:
            return response.text
        else:
            if response.prompt_feedback:
                st.warning(f"O prompt foi bloqueado. Razão: {response.prompt_feedback.block_reason}")
                if response.prompt_feedback.safety_ratings:
                    for rating in response.prompt_feedback.safety_ratings:
                        st.caption(f"Categoria: {rating.category}, Probabilidade: {rating.probability}")
            return "A IA não pôde gerar uma resposta para este prompt. Verifique as mensagens acima ou tente reformular seu pedido."
    except Exception as e:
        st.error(f"Erro ao gerar resposta da IA: {str(e)}")
        if hasattr(e, 'message'): 
            st.error(f"Detalhe da API Gemini: {e.message}")
        return None

st.set_page_config(page_title="Exercício", page_icon="🚀")

st.title("Criador de Histórias com Gemini")

nome_protagonista = st.text_input("Nome do protagonista: ")

opcoes_generos = ["Aventura", "Fantasia", "Ficção Científica", "Mistério", "Romance", "Terror"]
opcoes_locais = ["Floresta Assombrada", "Cidade Futurista", "Nave Espacial", "Uma Praça", "Um Shopping"]

genero = st.selectbox("Qual o gênero?", opcoes_generos)

local_inicial = st.radio("Qual o primeiro local da história?", opcoes_locais )

frase_efeito = st.text_area("Frase de Efeito ou Desafio Inicial", placeholder="Ex: 'E de repente, tudo ficou escuro', ou 'O mapa indicava um perigo iminente'....")

if st.button("Gerar História"):
    if not nome_protagonista:
        st.warning("Escolha o nome do protagonista!")
    elif not opcoes_generos:
        st.warning("Escolha o gênero!")
    elif not opcoes_locais:
        st.warning("Escolha o local!")
    elif not frase_efeito:
        st.warning("Digite uma frase de efeito ou desafio!")
    else:
        prompt_completo = (
            f"Preciso de ajuda para escrever uma história. O nome do personagem principal é {nome_protagonista}. \n"
            f"O gênero que desejo para essa história é: {genero}.\n"
            f"Quero também que a história inicie em {local_inicial}.\n"
            f"Por fim, quero que o personagem diga a seguinte frase de efeito ou passe pelo desafio: {frase_efeito}"
        )


        st.markdown("---")
        st.markdown("⚙️ **Prompt que será enviado para a IA (para fins de aprendizado):**")
        st.text_area("",prompt_completo, height=250)
        st.markdown("---")

        st.spinner("A IA está gerando a história que você deseja...")

        resposta_ia = gerar_resposta_gemini(prompt_completo)

        if resposta_ia:
            st.markdown("Sugestão de História da IA:")
            st.markdown(resposta_ia)
        else:
            st.warning("Não foi possível carregar sua história :(, tente novamente!")