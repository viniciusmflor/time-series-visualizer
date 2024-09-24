import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Importando os dados
# Corrigido: Adicionada a opção 'parse_dates=['date']' para converter a coluna 'date' em um índice de datas (DatetimeIndex)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date', parse_dates=['date'])

# Limpando os dados (removendo outliers)
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
    df_line = df.copy()

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df_line.index, df_line['value'], color='red', linewidth=1)  # Corrigido

    # Definindo os títulos e rótulos
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
  

    # Salvar a figura
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.strftime('%B')  # Converte para nomes completos dos meses

    # Define a ordem dos meses de janeiro a dezembro
    month_order = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    df_bar['month'] = pd.Categorical(df_bar['month'], categories=month_order, ordered=True)

    # Agrupando os dados por 'year' e 'month' para calcular a média das visualizações mensais
    df_bar_grouped = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Criando o gráfico de barras
    fig, ax = plt.subplots(figsize=(12, 6))
    df_bar_grouped.plot(kind='bar', ax=ax)

    ax.set_title('Average Page Views per Month')
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.legend(title='Months')  # Define o título da legenda

    # Salvar a figura
    fig.savefig('bar_plot.png')
    return fig
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.strftime('%B')  # Converte para nomes completos dos meses

    df_bar_grouped = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    fig, ax = plt.subplots(figsize=(12, 6))
    df_bar_grouped.plot(kind='bar', ax=ax)

    ax.set_title('Average Page Views per Month')
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.legend(title='Months')  # Define o título da legenda

    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = df_box['date'].dt.year
    #  Uso de '.dt.strftime('%b')' para formatar os meses como abreviações (Jan, Feb, etc.)
    df_box['month'] = df_box['date'].dt.strftime('%b')

    # Definindo a ordem dos meses
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    #Criando duas subplots para os gráficos de caixas, garantindo que ambos sejam desenhados corretamente
    fig, axes = plt.subplots(1, 2, figsize=(18, 6))

    # boxplot anual
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    # Gráfico de caixa mensal
    # Corrigido: Uso do parâmetro 'order' para definir a ordem correta dos meses
    sns.boxplot(x='month', y='value', data=df_box, order=month_order, ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    # Salvando a figura
    fig.savefig('box_plot.png')
    return fig

# Chamando as funções para gerar os gráficos e salvá-los
draw_line_plot()
draw_bar_plot()
draw_box_plot()