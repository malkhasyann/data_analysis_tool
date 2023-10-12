import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px


st.set_page_config(
    page_icon='📊',
    page_title='Look At Your Data'
)

@st.cache_data
def load_data(file):
    if file is None:
        return None

    fname = file.name
    ext = fname.split('.')[-1]
    if ext == 'csv':
        return pd.read_csv(file)
    if ext == 'xlsx':
        return pd.read_excel(file)
    if ext == 'json':
        return pd.read_json(file)
    

def find_file_by_name(fname, files):
    for file in files:
        if file.name == fname:
            return file
    return None
    

LOADED_DATA = {}  # file name: dataframe
current_df: pd.DataFrame | None = None  # current dataframe object to work with

st.title('📊 Look At Your Data')

main_tab, visual_tab = st.tabs(['Statistics', 'Visualize'])

with main_tab:
    st.subheader('Load your datasets here')

    uploader_col, select_col = st.columns([0.7, 0.3])

    with uploader_col:
        uploader = st.file_uploader(
            label='Drop you files here',
            accept_multiple_files=True,
            key='uploader',
            label_visibility='collapsed',
            type=['csv', 'xlsx', 'json'],
            on_change=None
        )  # list of uploaded files

    with select_col:
        selected_file = st.selectbox(
            label='Choose the dataset to work with',
            options=[file.name for file in st.session_state['uploader']],
            key='selected_file'
        )

    name_placeholder = st.empty()  # placeholder for the active dataset name

    if st.session_state['selected_file']:  # activate selected dataset
        active_df_name = st.session_state['selected_file']
        name_placeholder.subheader(active_df_name)
        LOADED_DATA[active_df_name] = load_data(find_file_by_name(active_df_name, uploader))
        current_df = LOADED_DATA[active_df_name]

    if current_df is None:  # wait untill the dataset is uploaded
        st.stop()


    opt1, opt2, opt3 = st.columns(3)  # first column level for highlighting options

    # initialize checkbox keys in the session state
    if 'missing_cb' not in st.session_state:
        st.session_state['missing_cb'] = False
    if 'max_cb' not in st.session_state:
        st.session_state['max_cb'] = False
    if 'min_cb' not in st.session_state:
        st.session_state['min_cb'] = False

    current_df_view = current_df.copy().style

    # utility functions for highlighting dataframe view
    def highlight_max(s:pd.Series, props=''):
        return np.where(s == np.nanmax(s[s.notnull()]), props, '')
    def highlight_min(s:pd.Series, props=''):
        return np.where(s == np.nanmin(s[s.notnull()]), props, '')
    def highlight_null(s:pd.Series, props=''):
        return np.where(s.isna(), props, '')

    # activate highlightings if they are checked
    if st.session_state['missing_cb']:
        current_df_view = current_df_view.apply(highlight_null, axis=0, props='background-color:red')
    if st.session_state['min_cb']:
        current_df_view = current_df_view.apply(highlight_min, axis=0, props='background-color:blue')
    if st.session_state['max_cb']:
        current_df_view = current_df_view.apply(highlight_max, axis=0, props='background-color:purple')

    # show the dataframe view
    st.dataframe(
        current_df_view,
        use_container_width=True,
    )

    # adding checkboxes for highlighting
    with opt1:
        missing_cb = st.checkbox(
            label='🔴 Highlight missing values',
            key='missing_cb'
            )
    with opt2:
        min_cb = st.checkbox(
            label='🔵 Highlight min values',
            key='min_cb'
            )
    with opt3:
        max_cb = st.checkbox(
            label='🟣 Highlight max values',
            key='max_cb'
            )


    # general statistics under the dataframe

    mcol1, mcol2, mcol3 = st.columns(3)  # columns for metrics
    with mcol1:
        selected_column = st.selectbox(
            label='Choose the column to see null value metrics for each column',
            options=current_df.columns,
            key='selected_column'
        )
    with mcol2:
        delta = current_df[selected_column].dropna().shape[0] - current_df.shape[0]
        st.metric(
            label='Total number of rows',
            value=current_df.shape[0],
            delta=delta
        )
    with mcol3:
        st.metric(
            label='Total number of columns',
            value=current_df.shape[1]
        )

    col_tabs = st.tabs(tabs=list(current_df.columns))
    for tab, name in zip(col_tabs, current_df.columns):
        with tab:
            st.table(current_df[name].describe())


with visual_tab:
    st.header('Use charts to visualize the data')

    # plotly chart types we use
    # 1. px.line + px.area (with checkbox) -- numerical data : DONE
    # 2. px.bar  -- for categorical data
    # 3. px.histogram -- for quantitive data
    #       histogram can be used with a single Series,
    #       with two series as graph axes
    # 4. px.scatter
    #       example: px.scatter(df, x='Price', y='Manufacturer', color='Manufacturer')
    #
    # FUTURE FEATURE: px.line_3d(x, y, z)

    # line+area section
    st.subheader('Line Chart')
    line_cols = st.columns([0.4, 0.4, 0.2])  # x box, y box, area box

    with line_cols[0]:
        x_line = st.selectbox(
            label='Select Line X-axis',
            options=current_df.columns,
            placeholder='Select X-axis',
            label_visibility='collapsed'
        )
    with line_cols[1]:
        y_line = st.selectbox(
            label='Select Line Y-axis',
            options=current_df.columns,
            placeholder='Select Y-axis',
            label_visibility='collapsed'
        )
    with line_cols[2]:
        area_line = st.checkbox(label='Area')

    if area_line:
        # st.area_chart(current_df, x=x_line, y=y_line)
        fig = px.area(current_df, x=x_line, y=y_line)
        st.plotly_chart(fig, use_container_width=True)
    else:
        # st.line_chart(current_df, x=x_line, y=y_line)
        fig = px.line(current_df, x=x_line, y=y_line)
        st.plotly_chart(fig, use_container_width=True)

    # bar section
    st.subheader('Bar Chart')
    bar_cols = st.columns(2)  # x box, y box, area box

    with bar_cols[0]:
        x_bar = st.selectbox(
            label='Select Bar X-axis',
            options=current_df.columns,
            placeholder='Select X-axis',
            label_visibility='collapsed'
        )
    with bar_cols[1]:
        y_bar = st.selectbox(
            label='Select Bar Y-axis',
            options=current_df.columns,
            placeholder='Select Y-axis',
            label_visibility='collapsed'
        )

    fig = px.bar(current_df, x=x_bar, y=y_bar)
    st.plotly_chart(fig)

    # histogram section
    st.subheader('Histogram Chart')
    hist_cols = st.columns(2)  # x box, y box, area box

    with hist_cols[0]:
        x_hist = st.selectbox(
            label='Select Hist X-axis',
            options=current_df.columns,
            placeholder='Select X-axis',
            label_visibility='collapsed'
        )
    with hist_cols[1]:
        y_hist = st.selectbox(
            label='Select Hist Y-axis',
            options=current_df.columns,
            placeholder='Select Y-axis',
            label_visibility='collapsed'
        )

    fig = px.histogram(current_df, x=x_hist, y=y_hist)
    st.plotly_chart(fig)

    # scatter section
    st.subheader('Scatter Chart')
    scatter_cols = st.columns([0.3, 0.3, 0.25, 0.15])  # x box, y box, color box

    with scatter_cols[0]:
        x_scatter = st.selectbox(
            label='Select scatter X-axis',
            options=current_df.columns,
            placeholder='Select X-axis',
            label_visibility='collapsed'
        )
    with scatter_cols[1]:
        y_scatter = st.selectbox(
            label='Select scatter Y-axis',
            options=current_df.columns,
            placeholder='Select Y-axis',
            label_visibility='collapsed'
        )
    with scatter_cols[2]:
        scatter_color = st.selectbox(
            label='Scatter Color Selector',
            options=[None, x_scatter, y_scatter],
            label_visibility='collapsed'
        )
    with scatter_cols[3]:
        st.subheader('Color')
    fig = px.scatter(current_df, x=x_scatter, y=y_scatter, color=scatter_color)
    st.plotly_chart(fig)