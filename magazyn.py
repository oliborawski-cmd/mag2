import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- KONFIGURACJA STRONY ---
st.set_page_config(
    page_title="📊 Dashboard Magazynowy",
    page_icon="🏭",
    layout="wide"
)

# --- GENEROWANIE PRZYKŁADOWYCH DANYCH ---
# W prawdziwej aplikacji te dane pobierałbyś z bazy danych lub pliku Excel
def get_data():
    data = {
        'Produkt': ['Śruby M8', 'Nakrętki M8', 'Wiertarka Bosch', 'Młotek', 'Klej montażowy', 
                    'Piła tarczowa', 'Kask ochronny', 'Rękawice robocze', 'Szlifierka', 'Farba biała'],
        'Kategoria': ['Akcesoria', 'Akcesoria', 'Elektronarzędzia', 'Narzędzia ręczne', 'Chemia', 
                      'Elektronarzędzia', 'BHP', 'BHP', 'Elektronarzędzia', 'Chemia'],
        'Ilość': [1200, 850, 15, 40, 5, 8, 50, 200, 3, 12],
        'Min_Stan': [500, 500, 10, 20, 20, 5, 30, 100, 5, 20],
        'Cena_jedn': [0.50, 0.20, 450.00, 35.00, 25.00, 300.00, 40.00, 15.00, 220.00, 80.00]
    }
    df = pd.DataFrame(data)
    # Obliczenie wartości magazynu
    df['Wartość całkowita'] = df['Ilość'] * df['Cena_jedn']
    # Status zapasów
    df['Status'] = df.apply(lambda x: '⚠️ Krytyczny' if x['Ilość'] <= x['Min_Stan'] else '✅ OK', axis=1)
    return df

df = get_data()

# --- PASEK BOCZNY (FILTRY) ---
with st.sidebar:
    st.header("🔍 Filtrowanie")
    
    # Filtr kategorii
    all_categories = df['Kategoria'].unique().tolist()
    selected_categories = st.multiselect("Wybierz kategorię:", all_categories, default=all_categories)
    
    # Filtr statusu
    status_filter = st.radio("Pokaż status:", ["Wszystkie", "Tylko Krytyczne"])
    
    st.info("Powyższe filtry aktualizują wykresy w czasie rzeczywistym.")

# --- LOGIKA FILTROWANIA ---
df_filtered = df[df['Kategoria'].isin(selected_categories)]

if status_filter == "Tylko Krytyczne":
    df_filtered = df_filtered[df_filtered['Status'] == '⚠️ Krytyczny']

# --- GŁÓWNY DASHBOARD ---
st.title("🏭 Wizualny Dashboard Magazynu")
st.markdown("---")

# 1. SEKCJA KPI (Kluczowe Wskaźniki)
col1, col2, col3, col4 = st.columns(4)

total_items = df_filtered['Ilość'].sum()
total_value = df_filtered['Wartość całkowita'].sum()
low_stock_count = len(df_filtered[df_filtered['Status'] == '⚠️ Krytyczny'])
unique_items = len(df_filtered)

col1.metric("📦 Łączna ilość sztuk", f"{total_items:,.0f}")
col2.metric("💰 Wartość magazynu", f"{total_value:,.2f} PLN")
col3.metric("🚨 Niskie stany", low_stock_count, delta="-Alert" if low_stock_count > 0 else "Ok", delta_color="inverse")
col4.metric("🏷️ Liczba produktów", unique_items)

st.markdown("---")

# 2. SEKCJA WYKRESÓW (Górny rząd)
col_chart1, col_chart2 = st.columns([2, 1])

with col_chart1:
    st.subheader("📊 Stan magazynowy wg Produktów")
    # Wykres słupkowy z kolorowaniem wg statusu
    fig_bar = px.bar(
        df_filtered, 
        x='Produkt', 
        y='Ilość', 
        color='Status',
        color_discrete_map={'✅ OK': '#2ecc71', '⚠️ Krytyczny': '#e74c3c'},
        hover_data=['Min_Stan', 'Kategoria'],
        text='Ilość',
        title="Aktualna ilość vs Minimum"
    )
    # Dodanie linii minimalnego stanu (dla wizualizacji)
    fig_bar.update_traces(textposition='outside')
    st.plotly_chart(fig_bar, use_container_width=True)

with col_chart2:
    st.subheader("🍰 Udział Kategorii")
    # Wykres kołowy (Donut chart)
    fig_pie = px.donut(
        df_filtered, 
        values='Wartość całkowita', 
        names='Kategoria', 
        title='Wartość magazynu wg Kategorii',
        hole=0.4
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# 3. SEKCJA WYKRESÓW I TABELI (Dolny rząd)
col_chart3, col_table = st.columns([1, 2])

with col_chart3:
    st.subheader("📉 Poziom zapełnienia")
    # Wykres punktowy (Scatter) pokazujący relację ceny do ilości
    fig_scatter = px.scatter(
        df_filtered,
        x='Ilość',
        y='Cena_jedn',
        size='Wartość całkowita',
        color='Kategoria',
        hover_name='Produkt',
        log_x=True, # Skala logarytmiczna dla czytelności przy dużych różnicach ilości
        title="Analiza: Ilość vs Cena (wielkość = wartość)"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with col_table:
    st.subheader("📋 Szczegółowe dane")
    # Stylizowana tabela z Pandas
    st.dataframe(
        df_filtered.style.applymap(
            lambda v: 'color: red; font-weight: bold;' if v == '⚠️ Krytyczny' else 'color: green;', 
            subset=['Status']
        ).format({"Cena_jedn": "{:.2f} zł", "Wartość całkowita": "{:.2f} zł"}),
        use_container_width=True,
        height=350
    )
