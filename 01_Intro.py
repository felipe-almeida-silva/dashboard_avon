import streamlit as st

# config page
st.set_page_config(
    page_title="Dashboard VBHC Avon",
    layout="wide",
    initial_sidebar_state="auto",
)


# get avon logo from url
avon_logo = 'https://i.pinimg.com/originals/02/ed/30/02ed3038ba6235975923501f864519ce.png'
vital_logo = 'logo_Prancheta 1.png'
vbhc_logo = 'academia-vbhc-logo.webp'
dor_lomar = 'https://static.vecteezy.com/ti/vetor-gratis/p2/3239831-fisioterapia-exercicios-para-dor-lombar-infografico-vetor.jpg'

col1, col2 = st.columns(2)
col1.image(avon_logo, width=350, use_column_width=True)
col2.image(vital_logo, width=350, use_column_width=True)

st.markdown('A empresa Avon é uma das maiores empresas de vendas diretas de cosméticos e produtos para o lar do mundo. Fundada em 1886, a Avon tem uma presença global e oferece uma ampla gama de produtos, incluindo maquiagem, cuidados com a pele, fragrâncias e produtos para o lar.')

st.image(vbhc_logo, width=150)
st.markdown('O Valor ao Longo da Cadeia de Saúde (VBHC, na sigla em inglês) é uma abordagem para a gestão da saúde que busca maximizar o valor para o paciente, considerando não apenas os custos dos tratamentos, mas também a qualidade de vida dos pacientes e sua satisfação com os resultados.')

st.image(dor_lomar, width=150)
st.markdown('Atendimentos terapêuticos para dor lombar incluem uma ampla gama de abordagens, como fisioterapia, acupuntura, terapia ocupacional e medicamentos, entre outros. O objetivo é aliviar a dor e ajudar a prevenir futuras lesões. É importante consultar um médico ou um terapeuta para determinar o melhor tratamento para a dor lombar individual.')

# center avon logo vertically using st.markdown


st.markdown('''
<style>
[data-testid=stImage]{
            vertical-align: middle;
        }
</style>
    ''', unsafe_allow_html=True)