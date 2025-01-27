import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
import streamlit as st
from os import pipe
import timeit


custom_params = {"axes.spines.right": False, "axes.spines.top": False}
sns.set_theme(style="ticks", rc=custom_params)
 
# FUNÇÃO PARA LEITURA DOS DADOS - @ST.CACHE
@st.cache_data(show_spinner = True)
def load_data(file_data):
  try:
      return pd.read_csv(file_data, sep = ';')
  except:
      return pd.read_excel(file_data, sep = ',')

# FUNÇÃO PARA FILTROS COM OPÇÃO "ALL"
@st.cache_data
def multiselect_filter(relatorio, col, selecionados):
  if 'all' in selecionados:
    return relatorio
  else:
    return relatorio[relatorio[col].isin(selecionados)].reset_index(drop=True)
 
# FUNÇÃO PARA CONVERTER DF PARA CSV
@st.cache_data
def df_toString(df):
    return df.to_csv(index=False).encode('utf-8')
 
# FUNÇÃO PARA CONVERTER DF PARA EXCEL
@st.cache_data
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data
 
# FUNÇÃO PRINCIPAL DO APP
def main():
  st.set_page_config(page_title = 'Telemarketing analisys',
      page_icon = 'telmarketing_icon.png',
      layout = 'wide',
      initial_sidebar_state = 'expanded'
  )
 
  # TÍTULO PRINCIPAL DO APP
  st.title('Telemarketing analisys')
  st.markdown("---")
 
  # APRESENTA UMA IMAGEM
  image = Image.open('Bank-Branding.jpg')
  st.sidebar.image(image)
 
  # BOTÃO PARA CARREGAR UM ARQUIVO NO APP
  st. sidebar.write("## Upload file")
  data_file_1 = st.sidebar.file_uploader("Bank marketing data", type=['csv', 'xlsx'])
 
  # VERIFICANDO SE HÁ CONTEÚDO CARREGADO NO APP
  if (data_file_1 is not None):
    start = timeit.default_timer()
    bank_raw = load_data(data_file_1)
 
    st.write('Time: ', timeit.default_timer() - start)
    bank = bank_raw.copy()
 
    st.write('## Before filters')
    st.write(bank_raw.head())
 
    with st.sidebar.form(key = 'my_form'):
 
        # SELECIONANDO O TIPO DE GRÁFICO
        graph_type = st.radio('Graph type: ', ('Bars', 'Pie'))
 
        # IDADES
        max_age = int(bank.age.max())
        min_age = int(bank.age.min())
        idades = st.slider(label = 'Age',
                           min_value = min_age,
                           max_value = max_age,
                           value = (min_age, max_age),
                           step = 1)
 
        # PROFISSÕES
        jobs_list = bank.job.unique().tolist()
        jobs_list.append('all')
        jobs_selected = st.sidebar.multiselect("Job", jobs_list, ['all'])
 
        # ESTADO CIVIL
        marital_list = bank.marital.unique().tolist()
        marital_list.append('all')
        marital_selected = st.sidebar.multiselect("Marital status", marital_list, ['all'])
 
        # DEFAUT?
        default_list = bank.default.unique().tolist()
        default_list.append('all')
        default_selected = st.sidebar.multiselect("Defaut?", default_list, ['all'])
 
        # TEM FINANCIAMENTO IMOBILIÁRIO?
        housing_list = bank.housing.unique().tolist()
        housing_list.append('all')
        housing_selected = st.sidebar.multiselect("Housing?", housing_list, ['all'])
 
        # TEM EMPRÉSTIMO?
        loan_list = bank.loan.unique().tolist()
        loan_list.append('all')
        loan_selected = st.sidebar.multiselect("Any loan?", loan_list, ['all'])

        # MEIO DE CONTATO
        contact_list = bank.contact.unique().tolist()
        contact_list.append('all')
        contact_selected = st.sidebar.multiselect("Contact info", contact_list, ['all'])
 
        # MÊS DO CONTATO
        month_list = bank.month.unique().tolist()
        month_list.append('all')
        month_selected = st.sidebar.multiselect("Contact month", month_list, ['all'])
 
        # DIA DA SEMANA
        day_of_week_list = bank.day_of_week.unique().tolist()
        day_of_week_list.append('all')
        day_of_week_selected = st.sidebar.multiselect("Days of the week", day_of_week_list, ['all'])
 
        bank = (bank.query("age >= @idades[0] and age <= @idades[1]")
                    .pipe(multiselect_filter, 'job', jobs_selected)
                    .pipe(multiselect_filter, 'marital', marital_selected)
                    .pipe(multiselect_filter, 'default', default_selected)
                    .pipe(multiselect_filter, 'housing', housing_selected)
                    .pipe(multiselect_filter, 'loan', loan_selected)
                    .pipe(multiselect_filter, 'contact', contact_selected)
                    .pipe(multiselect_filter, 'month', month_selected)
                    .pipe(multiselect_filter, 'day_of_week', day_of_week_selected)
        )
 
        submit_button = st.form_submit_button(label = 'Apply filters')


    # BOTÕES DE DOWNLOAD DOS DADOS FILTRADOS
    st.write('## After filters')
    st.write(bank.head())
 
    csv = df_toString(bank_raw)
    st.write(type(csv))
    st.write(csv[:100])

    st.write('### Download CSV')

    st.download_button(
      label="Download data as CSV",
      data=csv,
      file_name='bank-data-filtered.csv',
      mime='text/csv',
    )
 
    df_xlsx = to_excel(bank)
    st.write(type(df_xlsx))
    st.write(df_xlsx[:100])
 
    st.write('### Download Excel')
    st.download_button(label='Download data as Excel',
                      data=df_xlsx,
                      file_name='bank-data-filtered.xlsx')
    st.markdown("---")
 
    # GRÁFICOS
    fig, ax = plt.subplots(1, 2, figsize = (5,3))

    bank_raw_target_perc = bank_raw.y.value_counts(normalize = True).to_frame()*100
    bank_raw_target_perc = bank_raw_target_perc.sort_index()
 
    try:
        bank_target_perc = bank.y.value_counts(normalize = True).to_frame()*100
        bank_target_perc = bank_target_perc.sort_index()
    except:
        st.error('Filter error!')
 
    # BOTÕES DE DOWNLOAD DOS GRÁFICOS
    col1, col2 = st.columns(2)
 
    df_xlsx = to_excel(bank_target_perc)
    col1.write('### Original data')
    col1.write(bank_raw_target_perc)
    col1.download_button(label='Download',
                        data=df_xlsx,
                        file_name='bank_raw_y.xlxs')
 
    df_xlsx = to_excel(bank_target_perc)
    col1.write('### Filtered data')
    col1.write(bank_raw_target_perc)
    col1.download_button(label='Download',
                        data=df_xlsx,
                        file_name='bank_y.xlxs')
    st.markdown("---")
 
    st.write('## Acceptance ratio')
    # PLOTS
    if graph_type == 'Bars':
        sns.barplot(x = bank_raw_target_perc.index,
                    y = 'y',
                    data = bank_raw_target_perc,
                    ax = ax[0])
        ax[1].bar_label(ax[1].containers[0])
        ax[1].set_title('Raw data',
                      fontweight ="bold")
 
        sns.barplot(x = bank_target_perc.index,
                  y = 'y',
                  data = bank_target_perc,
                  ax = ax[1])
        ax[1].bar_label(ax[1].containers[0])
        ax[1].set_title('Filtered data',
                      fontweight ="bold")
    else:
        bank_raw_target_perc.plot(kind = 'pie', autopct = '%.2f', y = 'y', ax = ax[0])
        ax[0].set_title('Raw data',
                      fontweight ="bold")
 
        bank_target_perc.plot(kind = 'pie', autopct = '%.2f', y = 'y', ax = ax[1])
        ax[1].set_title('Filtered data',
                      fontweight ="bold")
 
    st.pyplot(plt)
 
