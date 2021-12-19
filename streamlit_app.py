from re import template
from pkg_resources import run_script
from streamlit.state.session_state import SessionState
import streamlit as st
import pandas as pd

from sqlalchemy import create_engine
import psycopg2 as pg
import pandas.io.sql as psql

import plotly.express as px
import plotly.graph_objs as gobj

import sys
from streamlit import cli as stcli
import streamlit

# import keyboard
import os
# import signal

from PIL import Image

import pandas as pd
# from pandasgui import show

import plotly.graph_objects as go

import geopandas as gpd
import folium

from streamlit_folium import folium_static

import matplotlib.pyplot as plt
import descartes
from shapely.geometry import Point, Polygon

import numpy

import flask

### MAIN DASHBOARD ###

def dbrd():

    ## NO ERROR BUT NO IMAGE

    # page_bg_img = "<style>body{background-image:url('https://images.unsplash.com/photo-1542281286-9e0a16bb7366');background-size:cover;}</style>"

    # st.markdown(page_bg_img, unsafe_allow_html=True)

## WORKS BUT NOT GREAT LOOKING

#     st.markdown(
#     """
#     <style>
#     .reportview-container {
#         background: url("https://images.unsplash.com/photo-1542281286-9e0a16bb7366")
#     }
#    .sidebar .sidebar-content {
#         background: url("https://images.unsplash.com/photo-1542281286-9e0a16bb7366")
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

    app = flask.Flask(__name__)
    resources = flask.Flask(__name__, instance_path=app.root_path + "\Resources")
    mappath = flask.Flask(__name__, instance_path=app.root_path + "\Maps")

    if 'site' not in st.session_state:
        st.session_state.site = "None"

    # conn = pg.connect(host="SG-Globalstratos1-2053-pgsql-master.servers.mongodirector.com", 
    #     dbname="Globalstratos1", 
    #     user="sgpostgres", 
    #     password="rUMw2uAud&vh60qH",
    #     port="5432"
    # )

    conn = pg.connect(host="SG-Globalstratos1-2053-pgsql-master.servers.mongodirector.com", 
    dbname="identity", 
    user="sgpostgres", 
    password="rUMw2uAud&vh60qH" ,
    port="5432",
    sslmode= "verify-full",
    sslrootcert = os.path.join(app.instance_path, "scalegridsslcert")
)

    # conn2 = create_engine("postgresql+psycopg2://SG-Globalstratos1-2053-pgsql-master.servers.mongodirector.com:5432/identity",
    conn2 = create_engine("postgresql+psycopg2://sgpostgres:rUMw2uAud&vh60qH@SG-Globalstratos1-2053-pgsql-master.servers.mongodirector.com:5432/identity")
    connect_args={"sslmode":"verify-full", "sslrootcert": os.path.join(app.instance_path) + "/scalegridsslcert"}
    connection = conn2.raw_connection()
    cursor = connection.cursor()

    # preheader = st.container()
    header1 = st.container()
    header2 = st.container()
    dataset = st.container()
    features = st.container()
    siteinfo = st.container()
    overviewmap = st.container()
    model_training = st.container()

    # with preheader:

    #     col1, col2,col3, col4, col5 = st.columns(5)
    #     with col1:
    #         pass
    #     with col2:
    #         pass
    #     with col3:
    #         pass
    #     with col4:
    #         pass
    #     with col5:
    #         quitapp = st.button("Exit")

    def handle_click():
            st.session_state.foo = 'User training'

    with header1:
        
        clm1, clm2, clm3, clm4, clm5 = st.columns(5)
        with clm1:
            pass
        with clm2:
            pass
        with clm3:
            # image1 = Functions.set_svg_image('GSLogo.jpg')
            # image2 = Image.open(image1)
            # st.image(image2, width=283)
            pass
        with clm4:
            pass
        with clm5:
            trainuser = st.button("Show me how", on_click=handle_click, key="trainuser")

    with header2:
        #st.title('Globalstratos Dashboard')
        st.markdown("<h1 style='text-align: center; color: green;'>Main Globalstratos Dashboard</h1>", unsafe_allow_html=True)
        #st.text('This dashboard builds on a proprietary dataset gathered at source')
        st.markdown("<p style='text-align: center; color: white;'>This dashboard builds on a proprietary dataset gathered at source</p>", unsafe_allow_html=True)

    with dataset:

        st.header("")
        st.header("Data from primary collection")
        st.text("Data sourced during direct interactions, during identity onboarding and site assessments.")

        # dbcall()

        identity = pd.read_sql_query("SELECT * FROM public.identity",conn)
        sites = pd.read_sql_query("SELECT * FROM public.siteproductioninfo",conn)
        sitestranspose = sites.transpose()
        forms = pd.read_sql_query("SELECT * FROM public.generalformentry",conn)

        st.write('First 5 sample records:')

        st.write(identity.head())

        respondents = pd.read_sql_query("SELECT COUNT(uuid) FROM public.generalformentry WHERE form_name = 'Registration' GROUP BY today", conn)
        st.subheader("Number of registered identities")
        st.markdown('* We consider first the total number of registered participants - **formalization at scale**')
        st.line_chart(respondents)

    with features:

        header = st.container()
        content = st.container()

        with header:
            st.header("Origin countries of registered individuals")
            st.subheader("(top 3 African priorities)")

        with content:
            
            sel_col, empty_col, disp_col = st.columns(3)

            cursor.execute("SELECT COUNT(uuid) FROM public.identitydetails WHERE id_country = 'South Africa' GROUP BY id_country")
            zar = cursor.fetchall()
            cursor.execute("SELECT COUNT(uuid) FROM public.identitydetails WHERE id_country = 'Nigeria' GROUP BY id_country")
            nigr = cursor.fetchall()
            cursor.execute("SELECT COUNT(uuid) FROM public.identitydetails WHERE id_country = 'Kenya' GROUP BY id_country")
            kenr = cursor.fetchall()
            
            # data = dict(type = 'choropleth',
            #     locations = ['south africa','nigeria','kenya'],
            #     locationmode = 'country names',
            #     colorscale= 'Portland',
            #     text= ['ZA','NIG','KEN'],
            #     z=[(zar[0])[0], (nigr[0])[0], (kenr[0])[0]],
            #     colorbar = {'title':'Country intensity', 'len':200,'lenmode':'pixels'})
            # #template = 'plotly_dark'
            # layout = dict(geo = {'scope':'africa'})
            # data.colorbar.x=-0.1
            # sel_col.write(gobj.Figure(data = data,layout = layout))

            fig = go.Figure(data=go.Choropleth(
                locations=['south africa','nigeria','kenya'], # Spatial coordinates
                text= ['ZA','NIG','KEN'],
                z = [(zar[0])[0], (nigr[0])[0], (kenr[0])[0]], # Data to be color-coded
                locationmode = 'country names', # set of locations match entries in `locations`
                colorscale = 'Portland',
                colorbar_title = "Country intensity",
            ))

            cursor.execute("SELECT COUNT(which_province_state_is_the_site_located) FROM public.siteinfo WHERE which_province_state_is_the_site_located = 'Kaduna' GROUP BY which_province_state_is_the_site_located")
            kaduna = cursor.fetchall()

            fig.update_layout(
                title_text = 'Number of registered individuals by country',
                geo_scope='africa', # limit map scope to Africa
            )

            fig.data[0].colorbar.x=-0.1
            sel_col.write(fig)

            disp_col.markdown("<h3 style='text-align: center; color: black;'>The total number of registered individuals is:</h3>", unsafe_allow_html=True)
            disp_col.markdown("<h1 style='text-align: center; color: green;'>" + str(identity['uuid'].count()) + "</h1>", unsafe_allow_html=True)

            disp_col.markdown("<h3 style='text-align: center; color: black;'>The total number of registered sites is:</h3>", unsafe_allow_html=True)
            disp_col.markdown("<h1 style='text-align: center; color: green;'>" + str(sites['uuid'].count()) + "</h1>", unsafe_allow_html=True)

            disp_col.markdown("<h3 style='text-align: center; color: black;'>The total number of forms completed is:</h3>", unsafe_allow_html=True)
            disp_col.markdown("<h1 style='text-align: center; color: green;'>" + str(forms['uuid'].count()) + "</h1>", unsafe_allow_html=True)

    with siteinfo:
        clmn1, clmn2, clmn3 = st.columns(3)

        with clmn1:
            cursor.execute("SELECT DISTINCT(site_name) FROM public.siteproductioninfo")
            siteselections = cursor.fetchall()
            selectedsite = st.selectbox("More site information - please choose site", siteselections, key="differentsite")
            SessionState.selectedsite=selectedsite[0]
            print(selectedsite)
            def handle_click():
                st.session_state.foo = 'Specific site information'
                sitespecificinfo
            moresitedetails = st.button("Tell me more about this site", on_click=handle_click)
            moresitedetails2 = st.button("Let me analyze and compare sites")
            if moresitedetails2 == True:
                selectedsite = pd.read_sql_query('SELECT * FROM public.siteproductioninfo',conn)
                # gui=show(selectedsite)
            
        with clmn2:
            pass

        with clmn3:
            morepeopleinfo = st.button("More information on individuals")
            moresiteinfo = st.button("More information on sites")

            if morepeopleinfo == True:
                # gui1 = show(identity)
                pass

            if moresiteinfo == True:
                # gui2 = show(sites)
                pass

    with overviewmap:

        col = st.expander("More geographic information, including maps with site markers", expanded=False)

        with col:

            sitelocations = pd.read_sql_query("select distinct(site_location), site_name from public.siteinfo",conn)

            # print(sitelocations)

            for i in range(0, len(sitelocations['site_location'])):
                sitelocs = sitelocations['site_location'].str.split(' ', expand=True)
                sitelocations['lat'] = numpy.float16(sitelocs[0])
                sitelocations['long'] = numpy.float16(sitelocs[1])
            print(sitelocations['lat'])
            print(sitelocations['long'])
                # sitelocs[i][0] = float(sitelocs[i][0])
                # sitelocs[i][1] = float(sitelocs[i][1])

            # center on Abuja 
            m = folium.Map(location=[9.0765, 7.3986], zoom_start=3)

            # add marker for sites
            for i in range(0, len(sitelocations['site_location'])):
                tooltip = (sitelocations['site_name'])[i]
                folium.Marker(
                    [(sitelocations['lat'])[i], (sitelocations['long'])[i]], popup=(sitelocations['site_name'])[i], tooltip=tooltip
                    ).add_to(m)

            st.header("Overview map")

            st.write("Use scroll wheel to zoom in or out")

            # call to render Folium map in Streamlit
            folium_static(m)

    # This used to be advanced analytics section

    # if quitapp==True:
    #     keyboard.press_and_release('ctrl+w')
    #     os.kill(os.getpid(), signal.SIGTERM)

    # if za == True:
    #     SessionState.site = "South Africa"
    # elif nig == True:
    #     SessionState.site = "Nigeria"
    # elif ken == True:
    #     SessionState.site = "Kenya"
        
if __name__ == '__main__':
    if streamlit._is_running_with_streamlit:
        dbrd.run()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())
