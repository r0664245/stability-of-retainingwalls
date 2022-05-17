import streamlit as st
import pandas as pd
import math
import altair as alt
import numpy as np
from mathconversions import dg_rad
from mathconversions import rad_dg
import math
from mathconversions import s
from mathconversions import c
from mathconversions import s2
from mathconversions import c2
from mathconversions import bs
from mathconversions import t
from mathconversions import t2
from mathconversions import bt
from mathconversions import bt2
from mathconversions import ac
from kakp import KASR
from kakp import KPSR
from kakp import KAGR
from kakp import KPGR
from kakp import KAC
from kakp import KPC
from kakp import KPCK
from kakp import KAL
from kakp import KPL
from kakp import KAPS
from kakp import KAMB
from kakp import KPMB
from kakp import KAK
from kakp import KPK
from TotalForce import FKA
from TotalForce import FKP
from TotalForce import KAW
from Stressdistribution import sigma_v
from Stressdistribution import sigma_ha
from Stressdistribution import sigma_hp
from Stressdistribution import sigma_v_ps
from MO import th
from MO import moa
from MO import mop
from MO import compare
from MO import Pae
from MO import L
from MO import A
from MO import B
from MO import a
from MO import b
from MO import C
from MO import alpha
from MO import SV_AIL
from MO import SH_AIL
from MO import P_AIL
from MO import H_AIL
from MO import KEA_MKP
from MO import KEP_MKP
from MO import d1
from MO import d1_s
from MO import d2
from MO import theta_EA
from MO import theta_EP
from MO import Keq
from WaveProb import waveprob


st.title('The Stability of retaining walls')
mode = st.selectbox('What are you interested in',['Ka - Kp','Stress Distribution','Total Force','Dynamic calculations Mononbe-Okabe','Wave propagation'])

if mode == 'Ka - Kp':
    method = st.selectbox('Which method ?',
                           ['Simplified Rankine', 'General Rankine','Coulomb' , 'Caquot & Kerisel', 'Lancellotta',
                            'Paik & Salgado', 'Müller-Breslau', 'Kötter','Compare all the methods'])


#user inputs
    if method in [ 'General Rankine','Coulomb','Caquot & Kerisel']:

        beta = st.sidebar.slider('Inclination of the backfill (beta)',0,30,0)
        eta = st.sidebar.slider('Inclination of the wall surface (eta)',0,30,0)
        eta_r = dg_rad(eta)
        beta_r = dg_rad(beta)

    if method in [ 'Coulomb', 'Lancellotta'
                            , 'Müller-Breslau', 'Kötter']:
        delta = st.sidebar.checkbox('Display effects of delta')
    else:
        delta = False

#calculations based of methods
    list_phi_graph = []
    list_phi_table = []
    list_ka = []
    list_kp = []
    list_k = []
    legend = []
    list_ka_0 = []
    list_ka_1 = []
    list_ka_2 = []
    list_ka_3 = []
    list_kp_0 = []
    list_kp_1 = []
    list_kp_2 = []
    list_kp_3 = []

    if method == 'Simplified Rankine':

        for x in range(10,46):
            phi = dg_rad(x)
            ka = KASR(phi)
            kp = KPSR(phi)

            list_phi_graph.append(x)
            list_phi_graph.append(x)
            list_k.append(ka)
            list_k.append(kp)
            legend.append('ka')
            legend.append('kp')

            list_phi_table.append(x)
            list_ka.append(ka)
            list_kp.append(kp)

    if method == 'General Rankine':

        for x in range(10,46):
            phi = dg_rad(x)

            if x < beta:
                ka = 0
                kp = 0

            else:
                ka = KAGR(phi, beta_r, eta_r)
                kp = KPGR(phi, beta_r, eta_r)

                list_phi_graph.append(x)
                list_phi_graph.append(x)
                list_k.append(ka)
                list_k.append(kp)
                legend.append('ka')
                legend.append('kp')

                list_phi_table.append(x)
                list_ka.append(ka)
                list_kp.append(kp)

    if method == 'Coulomb':

        for x in range(10,46):

            if beta > x:
                ka = 0
                kp = 0
            else:
                phi = dg_rad(x)
                delta_r = [0, 0.25*phi,0.5*phi,0.75*phi]

                ka_0 = KAC(phi, beta_r, eta_r, delta_r[0])
                kp_0 = KPC(phi, beta_r, eta_r, delta_r[0])

                ka_1 = KAC(phi, beta_r, eta_r, delta_r[1])
                kp_1 = KPC(phi, beta_r, eta_r, delta_r[1])

                ka_2 = KAC(phi, beta_r, eta_r, delta_r[2])
                kp_2 = KPC(phi, beta_r, eta_r, delta_r[2])

                ka_3 = KAC(phi, beta_r, eta_r, delta_r[3])
                kp_3 = KPC(phi, beta_r, eta_r, delta_r[3])

                if delta:

                    list_phi_graph.append(x)
                    list_phi_graph.append(x)
                    list_phi_graph.append(x)
                    list_phi_graph.append(x)

                    list_ka.append(ka_0)
                    list_ka.append(ka_1)
                    list_ka.append(ka_2)
                    list_ka.append(ka_3)

                    list_kp.append(kp_0)
                    list_kp.append(kp_1)
                    list_kp.append(kp_2)
                    list_kp.append(kp_3)

                    legend.append('delta = 0')
                    legend.append('delta = 25% phi')
                    legend.append('delta = 50% phi')
                    legend.append('delta = 75% phi')

                    list_phi_table.append(x)

                    list_ka_0.append(ka_0)
                    list_ka_1.append(ka_1)
                    list_ka_2.append(ka_2)
                    list_ka_3.append(ka_3)

                    list_kp_0.append(kp_0)
                    list_kp_1.append(kp_1)
                    list_kp_2.append(kp_2)
                    list_kp_3.append(kp_3)

                else:
                    list_phi_graph.append(x)
                    list_phi_graph.append(x)
                    list_k.append(ka_0)
                    list_k.append(kp_0)
                    legend.append('ka')
                    legend.append('kp')

                    list_phi_table.append(x)
                    list_ka.append(ka_0)
                    list_kp.append(kp_0)

    if method == 'Caquot & Kerisel':
        delta = True

        for x in range(10,46):

            if beta > x:
                ka = 0
                kp = 0
            else:
                phi = dg_rad(x)
                delta_r = [0, 0.25*phi,0.5*phi,0.75*phi]

                kp_0 = KPCK(phi, beta_r, eta_r, delta_r[0])

                kp_1 = KPCK(phi, beta_r, eta_r, delta_r[1])

                kp_2 = KPCK(phi, beta_r, eta_r, delta_r[2])

                kp_3 = KPCK(phi, beta_r, eta_r, delta_r[3])

                list_phi_graph.append(x)
                list_phi_graph.append(x)
                list_phi_graph.append(x)
                list_phi_graph.append(x)

                list_kp.append(kp_0)
                list_kp.append(kp_1)
                list_kp.append(kp_2)
                list_kp.append(kp_3)

                legend.append('delta = 0')
                legend.append('delta = 25% phi')
                legend.append('delta = 50% phi')
                legend.append('delta = 75% phi')

                list_phi_table.append(x)

                list_kp_0.append(kp_0)
                list_kp_1.append(kp_1)
                list_kp_2.append(kp_2)
                list_kp_3.append(kp_3)
    if method == 'Lancellotta':

        for x in range(10,46):
            phi = dg_rad(x)
            delta_r = [0, 0.25 * phi, 0.5 * phi, 0.75 * phi]

            ka_0 = KAL(phi, delta_r[0])
            kp_0 = KPL(phi, delta_r[0])

            ka_1 = KAL(phi, delta_r[1])
            kp_1 = KPL(phi, delta_r[1])

            ka_2 = KAL(phi, delta_r[2])
            kp_2 = KPL(phi, delta_r[2])

            ka_3 = KAL(phi, delta_r[3])
            kp_3 = KPL(phi, delta_r[3])

            if delta:

                list_phi_graph.append(x)
                list_phi_graph.append(x)
                list_phi_graph.append(x)
                list_phi_graph.append(x)

                list_ka.append(ka_0)
                list_ka.append(ka_1)
                list_ka.append(ka_2)
                list_ka.append(ka_3)

                list_kp.append(kp_0)
                list_kp.append(kp_1)
                list_kp.append(kp_2)
                list_kp.append(kp_3)

                legend.append('delta = 0')
                legend.append('delta = 25% phi')
                legend.append('delta = 50% phi')
                legend.append('delta = 75% phi')

                list_phi_table.append(x)

                list_ka_0.append(ka_0)
                list_ka_1.append(ka_1)
                list_ka_2.append(ka_2)
                list_ka_3.append(ka_3)

                list_kp_0.append(kp_0)
                list_kp_1.append(kp_1)
                list_kp_2.append(kp_2)
                list_kp_3.append(kp_3)

            else:
                list_phi_graph.append(x)
                list_phi_graph.append(x)
                list_k.append(ka_0)
                list_k.append(kp_0)
                legend.append('ka')
                legend.append('kp')

                list_phi_table.append(x)
                list_ka.append(ka_0)
                list_kp.append(kp_0)

    if method == 'Paik & Salgado':
        for x in range(10,46):
            delta = False
            phi = dg_rad(x)
            delta_r = [0.1*phi, 0.25 * phi, 0.5 * phi, 0.75 * phi]

            ka_0 = KAPS(phi, delta_r[0])
            ka_1 = KAPS(phi, delta_r[1])
            ka_2 = KAPS(phi, delta_r[2])
            ka_3 = KAPS(phi, delta_r[3])

            list_phi_graph.append(x)
            list_phi_graph.append(x)
            list_phi_graph.append(x)
            list_phi_graph.append(x)

            list_ka.append(ka_0)
            list_ka.append(ka_1)
            list_ka.append(ka_2)
            list_ka.append(ka_3)

            legend.append('delta = 10% phi')
            legend.append('delta = 25% phi')
            legend.append('delta = 50% phi')
            legend.append('delta = 75% phi')

            list_phi_table.append(x)

            list_ka_0.append(ka_0)
            list_ka_1.append(ka_1)
            list_ka_2.append(ka_2)
            list_ka_3.append(ka_3)
    if method == 'Müller-Breslau':

        for x in range(10,46):
            phi = dg_rad(x)
            delta_r = [0, 0.25 * phi, 0.5 * phi, 0.75 * phi]

            ka_0 = KAMB(phi, delta_r[0])
            kp_0 = KPMB(phi, delta_r[0])

            ka_1 = KAMB(phi, delta_r[1])
            kp_1 = KPMB(phi, delta_r[1])

            ka_2 = KAMB(phi, delta_r[2])
            kp_2 = KPMB(phi, delta_r[2])

            ka_3 = KAMB(phi, delta_r[3])
            kp_3 = KPMB(phi, delta_r[3])

            if delta:

                list_phi_graph.append(x)
                list_phi_graph.append(x)
                list_phi_graph.append(x)
                list_phi_graph.append(x)

                list_ka.append(ka_0)
                list_ka.append(ka_1)
                list_ka.append(ka_2)
                list_ka.append(ka_3)

                list_kp.append(kp_0)
                list_kp.append(kp_1)
                list_kp.append(kp_2)
                list_kp.append(kp_3)

                legend.append('delta = 0')
                legend.append('delta = 25% phi')
                legend.append('delta = 50% phi')
                legend.append('delta = 75% phi')

                list_phi_table.append(x)

                list_ka_0.append(ka_0)
                list_ka_1.append(ka_1)
                list_ka_2.append(ka_2)
                list_ka_3.append(ka_3)

                list_kp_0.append(kp_0)
                list_kp_1.append(kp_1)
                list_kp_2.append(kp_2)
                list_kp_3.append(kp_3)

            else:
                list_phi_graph.append(x)
                list_phi_graph.append(x)
                list_k.append(ka_0)
                list_k.append(kp_0)
                legend.append('ka')
                legend.append('kp')

                list_phi_table.append(x)
                list_ka.append(ka_0)
                list_kp.append(kp_0)
    if method == 'Kötter':

        for x in range(10,46):
            phi = dg_rad(x)
            delta_r = [0, 0.25 * phi, 0.5 * phi, 0.75 * phi]

            ka_0 = KAK(phi, delta_r[0])
            kp_0 = KPK(phi, delta_r[0])

            ka_1 = KAK(phi, delta_r[1])
            kp_1 = KPK(phi, delta_r[1])

            ka_2 = KAK(phi, delta_r[2])
            kp_2 = KPK(phi, delta_r[2])

            ka_3 = KAK(phi, delta_r[3])
            kp_3 = KPK(phi, delta_r[3])

            if delta:

                list_phi_graph.append(x)
                list_phi_graph.append(x)
                list_phi_graph.append(x)
                list_phi_graph.append(x)

                list_ka.append(ka_0)
                list_ka.append(ka_1)
                list_ka.append(ka_2)
                list_ka.append(ka_3)

                list_kp.append(kp_0)
                list_kp.append(kp_1)
                list_kp.append(kp_2)
                list_kp.append(kp_3)

                legend.append('delta = 0')
                legend.append('delta = 25% phi')
                legend.append('delta = 50% phi')
                legend.append('delta = 75% phi')

                list_phi_table.append(x)

                list_ka_0.append(ka_0)
                list_ka_1.append(ka_1)
                list_ka_2.append(ka_2)
                list_ka_3.append(ka_3)

                list_kp_0.append(kp_0)
                list_kp_1.append(kp_1)
                list_kp_2.append(kp_2)
                list_kp_3.append(kp_3)

            else:
                list_phi_graph.append(x)
                list_phi_graph.append(x)
                list_k.append(ka_0)
                list_k.append(kp_0)
                legend.append('ka')
                legend.append('kp')

                list_phi_table.append(x)
                list_ka.append(ka_0)
                list_kp.append(kp_0)
    if method == 'Compare all the methods':
        delta_i = st.sidebar.slider('delta factor',0.1,0.75,0.5)
        list_k = []
        legend_ka = []
        legend_kp = []
        delta = True

        for x in range(10,46):
            phi = dg_rad(x)
            delta_r = phi*delta_i
            beta = 0
            eta = 0

            ka_c = KAC(phi,beta,eta,delta_r)
            ka_l = KAL(phi,delta_r)
            ka_ps = KAPS(phi,delta_r)
            ka_mb = KAMB(phi,delta_r)
            ka_k = KAK(phi,delta_r)

            kp_c = KPC(phi,beta,eta,delta_r)
            kp_ck = KPCK(phi,beta,eta,delta_r)
            kp_l = KPL(phi,delta_r)
            kp_mb = KPMB(phi,delta_r)
            kp_k = KPK(phi,delta_r)

            list_phi_graph.append(x)
            list_phi_graph.append(x)
            list_phi_graph.append(x)
            list_phi_graph.append(x)
            list_phi_graph.append(x)

            list_ka.append(ka_c)
            list_ka.append(ka_l)
            list_ka.append(ka_ps)
            list_ka.append(ka_mb)
            list_ka.append(ka_k)

            list_kp.append(kp_c)
            list_kp.append(kp_ck)
            list_kp.append(kp_l)
            list_kp.append(kp_mb)
            list_kp.append(kp_k)

            legend_ka.append('Coulomb')
            legend_ka.append('Lacellotta')
            legend_ka.append('Paik and Salgado')
            legend_ka.append('Muller-Breslau')
            legend_ka.append('Kötter')

            legend_kp.append('Coulomb')
            legend_kp.append('Caquot and Kerisel')
            legend_kp.append('Lacellotta')
            legend_kp.append('Muller-Breslau')
            legend_kp.append('Kötter')


#inserting data into dataframes

    if method == 'Compare all the methods':
        graph_ka = pd.DataFrame({'phi': list_phi_graph, 'ka': list_ka, 'legend': legend_ka})
        graph_kp = pd.DataFrame({'phi': list_phi_graph, 'kp': list_kp, 'legend': legend_kp})

    else:
        if method == 'Paik & Salgado':
            graph_ka = pd.DataFrame({'phi': list_phi_graph, 'ka': list_ka, 'legend': legend})
            table_ka = pd.DataFrame({'phi': list_phi_table, 'delta = 10% phi': list_ka_0, 'delta = 25% phi': list_ka_1,
                                     'delta = 50% phi': list_ka_2, '75% phi': list_ka_3})
            table_ka = table_ka.set_index('phi')
        else:
            if method == 'Caquot & Kerisel':
                graph_kp = pd.DataFrame({'phi': list_phi_graph, 'kp': list_kp, 'legend': legend})
                table_kp = pd.DataFrame({'phi': list_phi_table, 'delta = 0': list_kp_0, 'delta = 25% phi': list_kp_1,
                                         'delta = 50% phi': list_kp_2, '75% phi': list_kp_3})
                table_kp = table_kp.set_index('phi')
            else:
                if delta:
                    graph_ka = pd.DataFrame({'phi': list_phi_graph, 'ka': list_ka, 'legend': legend})
                    graph_kp = pd.DataFrame({'phi': list_phi_graph, 'kp': list_kp, 'legend': legend})

                    table_ka = pd.DataFrame(
                        {'phi': list_phi_table, 'delta = 0': list_ka_0, 'delta = 25% phi': list_ka_1,
                         'delta = 50% phi': list_ka_2, 'delta = 75% phi': list_ka_3})
                    table_ka = table_ka.set_index('phi')
                    table_kp = pd.DataFrame(
                        {'phi': list_phi_table, 'delta = 0': list_kp_0, 'delta = 25% phi': list_kp_1,
                         'delta = 50% phi': list_kp_2, 'delta = 75% phi': list_kp_3})
                    table_kp = table_kp.set_index('phi')

                else:
                    data_graph = pd.DataFrame({'phi': list_phi_graph, 'coefficient': list_k, 'legend': legend})

                    graph_ka = data_graph[data_graph.legend == 'ka']
                    graph_kp = data_graph[data_graph.legend == 'kp']

                    data_table = pd.DataFrame({'phi': list_phi_table, 'Ka': list_ka, 'Kp': list_kp})
                    data_table = data_table.set_index('phi')

#generating layout and graphs

    st.subheader(method)


    if method == 'Compare all the methods':
        chart_ka = (
            alt.Chart(graph_ka).mark_line().encode(
                y=alt.Y('ka', axis=alt.Axis(title='Ka')),
                x='phi',
                color=alt.Color('legend')

            ).properties(
                title='Ka in function of friction angle'
            )
        )
        st.altair_chart(chart_ka, use_container_width=True)

        chart_kp = (
            alt.Chart(graph_kp).mark_line().encode(
                y=alt.Y('kp', axis=alt.Axis(title='Kp')),
                x='phi',
                color=alt.Color('legend')

            ).properties(
                title='Kp in function of friction angle'
            )
        )
        st.altair_chart(chart_kp, use_container_width=True)


    else:
        if method == 'Paik & Salgado':
            chart_ka = (
                alt.Chart(graph_ka).mark_line().encode(
                    y=alt.Y('ka', axis=alt.Axis(title='Ka')),
                    x='phi',
                    color=alt.Color('legend')

                ).properties(
                    title='Ka in function of friction angle'
                )
            )
            st.altair_chart(chart_ka, use_container_width=True)
            st.text('some combinations of phi and delta are undetermined these values are put at 0')
            st.write('ka')
            st.table(data=table_ka)

        else:
            if method == 'Caquot & Kerisel':
                chart_kp = (
                    alt.Chart(graph_kp).mark_line().encode(
                        y=alt.Y('kp', axis=alt.Axis(title='Kp')),
                        x='phi',
                        color=alt.Color('legend')

                    ).properties(
                        title='Kp in function of friction angle'
                    )
                )
                st.altair_chart(chart_kp, use_container_width=True)
                st.write('kp')
                st.table(data=table_kp)
            else:
                if delta:
                    chart_ka = (
                        alt.Chart(graph_ka).mark_line().encode(
                            y=alt.Y('ka', axis=alt.Axis(title='Ka')),
                            x='phi',
                            color=alt.Color('legend')

                        ).properties(
                            title='Ka in function of friction angle'
                        )
                    )
                    st.altair_chart(chart_ka, use_container_width=True)

                    chart_kp = (
                        alt.Chart(graph_kp).mark_line().encode(
                            y=alt.Y('kp', axis=alt.Axis(title='Kp')),
                            x='phi',
                            color=alt.Color('legend')

                        ).properties(
                            title='Kp in function of friction angle'
                        )
                    )
                    st.altair_chart(chart_kp, use_container_width=True)

                    st.subheader('Tabulated results')
                    st.write('ka')
                    st.table(data=table_ka)
                    st.write('kp')
                    st.table(data=table_kp)

                else:
                    chart_ka = (
                        alt.Chart(graph_ka).mark_line().encode(
                            y=alt.Y('coefficient', axis=alt.Axis(title='Ka')),
                            x='phi',
                            color=alt.Color('legend')

                        ).properties(
                            title='Ka in function of friction angle'
                        )
                    )
                    st.altair_chart(chart_ka, use_container_width=True)

                    chart_kp = (
                        alt.Chart(graph_kp).mark_line().encode(
                            y=alt.Y('coefficient', axis=alt.Axis(title='Kp')),
                            x='phi',
                            color=alt.Color('legend')

                        ).properties(
                            title='Kp in function of friction angle'
                        )
                    )
                    st.altair_chart(chart_kp, use_container_width=True)

                    st.subheader('Tabulated results')
                    st.table(data=data_table)
if mode == 'Total Force':
    method = st.selectbox('Which method ?',
                           ['Simplified Rankine', 'General Rankine','Coulomb' , 'Caquot & Kerisel', 'Lancellotta',
                            'Paik & Salgado', 'Müller-Breslau', 'Kötter','Compare all the methods'])

    if method in [ 'General Rankine','Coulomb','Caquot & Kerisel']:

        beta = st.sidebar.slider('Inclination of the backfill (beta)',0,30,0)
        eta = st.sidebar.slider('Inclination of the wall surface (eta)',0,30,0)
        eta_r = dg_rad(eta)
        beta_r = dg_rad(beta)

    list_F = []
    list_Fa = []
    list_Fp = []
    list_phi = []
    legend = []

    H = st.sidebar.slider('Height of the wall [m]',1,20,10)
    gamma = st.sidebar.slider('Weigth of the soil [kN/m³]',15,30,20)

    if method == 'Simplified Rankine':

        for x in range(10,46):
            phi = dg_rad(x)
            ka = KASR(phi)
            kp = KPSR(phi)
            Fa = FKA(ka,H,gamma)
            Fp = FKP(kp,H,gamma)

            list_phi.append(x)
            list_phi.append(x)
            list_F.append(Fa)
            list_F.append(Fp)
            legend.append('Active Force')
            legend.append('Passive Force')


    if method == 'General Rankine':

        for x in range(10,46):
            phi = dg_rad(x)

            if x < beta:
                ka = 0
                kp = 0

            else:
                ka = KAGR(phi, beta_r, eta_r)
                kp = KPGR(phi, beta_r, eta_r)
                Fa = FKA(ka, H, gamma)
                Fp = FKP(kp, H, gamma)

                list_phi.append(x)
                list_phi.append(x)
                list_F.append(ka)
                list_F.append(kp)
                legend.append('Active Force')
                legend.append('Passive Force')

    if method == 'Coulomb':

        for x in range(10,46):

            if beta > x:
                ka = 0
                kp = 0
            else:
                phi = dg_rad(x)
                delta_r = [0, 0.25*phi,0.5*phi,0.75*phi]

                ka_0 = KAC(phi, beta_r, eta_r, delta_r[0])
                kp_0 = KPC(phi, beta_r, eta_r, delta_r[0])

                ka_1 = KAC(phi, beta_r, eta_r, delta_r[1])
                kp_1 = KPC(phi, beta_r, eta_r, delta_r[1])

                ka_2 = KAC(phi, beta_r, eta_r, delta_r[2])
                kp_2 = KPC(phi, beta_r, eta_r, delta_r[2])

                ka_3 = KAC(phi, beta_r, eta_r, delta_r[3])
                kp_3 = KPC(phi, beta_r, eta_r, delta_r[3])

                Fa_0 = FKA(ka_0, H, gamma)
                Fp_0 = FKP(kp_0, H, gamma)

                Fa_1 = FKA(ka_1, H, gamma)
                Fp_1 = FKP(kp_1, H, gamma)

                Fa_2 = FKA(ka_2, H, gamma)
                Fp_2 = FKP(kp_2, H, gamma)

                Fa_3 = FKA(ka_3, H, gamma)
                Fp_3 = FKP(kp_3, H, gamma)

                list_phi.append(x)
                list_phi.append(x)
                list_phi.append(x)
                list_phi.append(x)

                list_Fa.append(Fa_0)
                list_Fa.append(Fa_1)
                list_Fa.append(Fa_2)
                list_Fa.append(Fa_3)

                list_Fp.append(Fp_0)
                list_Fp.append(Fp_1)
                list_Fp.append(Fp_2)
                list_Fp.append(Fp_3)

                legend.append('delta = 0')
                legend.append('delta = 25% phi')
                legend.append('delta = 50% phi')
                legend.append('delta = 75% phi')

    if method == 'Caquot & Kerisel':
        delta = True

        for x in range(10,46):

            if beta > x:
                ka = 0
                kp = 0
            else:
                phi = dg_rad(x)
                delta_r = [0, 0.25*phi,0.5*phi,0.75*phi]

                kp_0 = KPCK(phi, beta_r, eta_r, delta_r[0])
                kp_1 = KPCK(phi, beta_r, eta_r, delta_r[1])
                kp_2 = KPCK(phi, beta_r, eta_r, delta_r[2])
                kp_3 = KPCK(phi, beta_r, eta_r, delta_r[3])

                Fp_0 = FKP(kp_0, H, gamma)
                Fp_1 = FKP(kp_1, H, gamma)
                Fp_2 = FKP(kp_2, H, gamma)
                Fp_3 = FKP(kp_3, H, gamma)

                list_phi.append(x)
                list_phi.append(x)
                list_phi.append(x)
                list_phi.append(x)

                list_Fp.append(Fp_0)
                list_Fp.append(Fp_1)
                list_Fp.append(Fp_2)
                list_Fp.append(Fp_3)

                legend.append('delta = 0')
                legend.append('delta = 25% phi')
                legend.append('delta = 50% phi')
                legend.append('delta = 75% phi')

    if method == 'Lancellotta':

        for x in range(10,46):
            phi = dg_rad(x)
            delta_r = [0, 0.25 * phi, 0.5 * phi, 0.75 * phi]

            ka_0 = KAL(phi, delta_r[0])
            kp_0 = KPL(phi, delta_r[0])

            ka_1 = KAL(phi, delta_r[1])
            kp_1 = KPL(phi, delta_r[1])

            ka_2 = KAL(phi, delta_r[2])
            kp_2 = KPL(phi, delta_r[2])

            ka_3 = KAL(phi, delta_r[3])
            kp_3 = KPL(phi, delta_r[3])

            Fa_0 = FKA(ka_0, H, gamma)
            Fp_0 = FKP(kp_0, H, gamma)

            Fa_1 = FKA(ka_1, H, gamma)
            Fp_1 = FKP(kp_1, H, gamma)

            Fa_2 = FKA(ka_2, H, gamma)
            Fp_2 = FKP(kp_2, H, gamma)

            Fa_3 = FKA(ka_3, H, gamma)
            Fp_3 = FKP(kp_3, H, gamma)

            list_phi.append(x)
            list_phi.append(x)
            list_phi.append(x)
            list_phi.append(x)

            list_Fa.append(Fa_0)
            list_Fa.append(Fa_1)
            list_Fa.append(Fa_2)
            list_Fa.append(Fa_3)

            list_Fp.append(Fp_0)
            list_Fp.append(Fp_1)
            list_Fp.append(Fp_2)
            list_Fp.append(Fp_3)

            legend.append('delta = 0')
            legend.append('delta = 25% phi')
            legend.append('delta = 50% phi')
            legend.append('delta = 75% phi')


    if method == 'Paik & Salgado':
        for x in range(10,46):
            delta = False
            phi = dg_rad(x)
            delta_r = [0.1*phi, 0.25 * phi, 0.5 * phi, 0.75 * phi]

            ka_0 = KAPS(phi, delta_r[0])
            ka_1 = KAPS(phi, delta_r[1])
            ka_2 = KAPS(phi, delta_r[2])
            ka_3 = KAPS(phi, delta_r[3])

            kaw_0 = KAW(ka_0,delta_r[0],KPSR(phi))
            kaw_1 = KAW(ka_1,delta_r[1],KPSR(phi))
            kaw_2 = KAW(ka_2,delta_r[2],KPSR(phi))
            kaw_3 = KAW(ka_3,delta_r[3],KPSR(phi))

            Fa_0 = FKA(kaw_0, H, gamma)
            Fa_1 = FKA(kaw_1, H, gamma)
            Fa_2 = FKA(kaw_2, H, gamma)
            Fa_3 = FKA(kaw_3, H, gamma)

            list_phi.append(x)
            list_phi.append(x)
            list_phi.append(x)
            list_phi.append(x)

            list_Fa.append(Fa_0)
            list_Fa.append(Fa_1)
            list_Fa.append(Fa_2)
            list_Fa.append(Fa_3)

            legend.append('delta = 10% phi')
            legend.append('delta = 25% phi')
            legend.append('delta = 50% phi')
            legend.append('delta = 75% phi')

    if method == 'Müller-Breslau':

        for x in range(10,46):
            phi = dg_rad(x)
            delta_r = [0, 0.25 * phi, 0.5 * phi, 0.75 * phi]

            ka_0 = KAMB(phi, delta_r[0])
            kp_0 = KPMB(phi, delta_r[0])

            ka_1 = KAMB(phi, delta_r[1])
            kp_1 = KPMB(phi, delta_r[1])

            ka_2 = KAMB(phi, delta_r[2])
            kp_2 = KPMB(phi, delta_r[2])

            ka_3 = KAMB(phi, delta_r[3])
            kp_3 = KPMB(phi, delta_r[3])

            Fa_0 = FKA(ka_0, H, gamma)
            Fp_0 = FKP(kp_0, H, gamma)

            Fa_1 = FKA(ka_1, H, gamma)
            Fp_1 = FKP(kp_1, H, gamma)

            Fa_2 = FKA(ka_2, H, gamma)
            Fp_2 = FKP(kp_2, H, gamma)

            Fa_3 = FKA(ka_3, H, gamma)
            Fp_3 = FKP(kp_3, H, gamma)

            list_phi.append(x)
            list_phi.append(x)
            list_phi.append(x)
            list_phi.append(x)

            list_Fa.append(Fa_0)
            list_Fa.append(Fa_1)
            list_Fa.append(Fa_2)
            list_Fa.append(Fa_3)

            list_Fp.append(Fp_0)
            list_Fp.append(Fp_1)
            list_Fp.append(Fp_2)
            list_Fp.append(Fp_3)

            legend.append('delta = 0')
            legend.append('delta = 25% phi')
            legend.append('delta = 50% phi')
            legend.append('delta = 75% phi')


    if method == 'Kötter':

        for x in range(10,46):
            phi = dg_rad(x)
            delta_r = [0, 0.25 * phi, 0.5 * phi, 0.75 * phi]

            ka_0 = KAK(phi, delta_r[0])
            kp_0 = KPK(phi, delta_r[0])

            ka_1 = KAK(phi, delta_r[1])
            kp_1 = KPK(phi, delta_r[1])

            ka_2 = KAK(phi, delta_r[2])
            kp_2 = KPK(phi, delta_r[2])

            ka_3 = KAK(phi, delta_r[3])
            kp_3 = KPK(phi, delta_r[3])

            Fa_0 = FKA(ka_0, H, gamma)
            Fp_0 = FKP(kp_0, H, gamma)

            Fa_1 = FKA(ka_1, H, gamma)
            Fp_1 = FKP(kp_1, H, gamma)

            Fa_2 = FKA(ka_2, H, gamma)
            Fp_2 = FKP(kp_2, H, gamma)

            Fa_3 = FKA(ka_3, H, gamma)
            Fp_3 = FKP(kp_3, H, gamma)

            list_phi.append(x)
            list_phi.append(x)
            list_phi.append(x)
            list_phi.append(x)

            list_Fa.append(Fa_0)
            list_Fa.append(Fa_1)
            list_Fa.append(Fa_2)
            list_Fa.append(Fa_3)

            list_Fp.append(Fp_0)
            list_Fp.append(Fp_1)
            list_Fp.append(Fp_2)
            list_Fp.append(Fp_3)

            legend.append('delta = 0')
            legend.append('delta = 25% phi')
            legend.append('delta = 50% phi')
            legend.append('delta = 75% phi')

    if method == 'Compare all the methods':
        delta_i = st.sidebar.slider('delta factor',0.1,0.75,0.5)
        list_Fa = []
        list_Fp = []
        list_phi = []
        legend_ka = []
        legend_kp = []

        for x in range(10,46):
            phi = dg_rad(x)
            delta_r = phi*delta_i
            beta = 0
            eta = 0

            ka_c = KAC(phi,beta,eta,delta_r)
            ka_l = KAL(phi,delta_r)
            ka_ps = KAPS(phi,delta_r)
            ka_mb = KAMB(phi,delta_r)
            ka_k = KAK(phi,delta_r)

            kp_c = KPC(phi,beta,eta,delta_r)
            kp_ck = KPCK(phi,beta,eta,delta_r)
            kp_l = KPL(phi,delta_r)
            kp_mb = KPMB(phi,delta_r)
            kp_k = KPK(phi,delta_r)

            Fa_c = FKA(ka_c, H, gamma)
            Fa_l = FKA(ka_l, H, gamma)
            Fa_ps = FKA(ka_ps, H, gamma)
            Fa_mb = FKA(ka_mb, H, gamma)
            Fa_k = FKA(ka_k, H, gamma)

            Fp_c = FKP(kp_c, H, gamma)
            Fp_ck = FKP(kp_ck, H, gamma)
            Fp_l = FKP(kp_l, H, gamma)
            Fp_mb = FKP(kp_mb, H, gamma)
            Fp_k = FKP(kp_k, H, gamma)

            list_phi.append(x)
            list_phi.append(x)
            list_phi.append(x)
            list_phi.append(x)
            list_phi.append(x)

            list_Fa.append(Fa_c)
            list_Fa.append(Fa_l)
            list_Fa.append(Fa_ps)
            list_Fa.append(Fa_mb)
            list_Fa.append(Fa_k)

            list_Fp.append(Fp_c)
            list_Fp.append(Fp_ck)
            list_Fp.append(Fp_l)
            list_Fp.append(Fp_mb)
            list_Fp.append(Fp_k)

            legend_ka.append('Coulomb')
            legend_ka.append('Lacellotta')
            legend_ka.append('Paik and Salgado')
            legend_ka.append('Muller-Breslau')
            legend_ka.append('Kötter')

            legend_kp.append('Coulomb')
            legend_kp.append('Caquot and Kerisel')
            legend_kp.append('Lacellotta')
            legend_kp.append('Muller-Breslau')
            legend_kp.append('Kötter')

#Putting results into dataframes

    if method == 'Compare all the methods':
        graph_ka = pd.DataFrame({'phi': list_phi, 'Active': list_Fa, 'legend': legend_ka})
        graph_kp = pd.DataFrame({'phi': list_phi, 'Passive': list_Fp, 'legend': legend_kp})
    else:
        if method == 'Caquot & Kerisel':
            graph_kp = pd.DataFrame({'phi': list_phi, 'Passive': list_Fp, 'legend': legend})
        else:
            if method == 'Paik & Salgado':
                graph_ka = pd.DataFrame({'phi': list_phi, 'Active': list_Fa, 'legend': legend})
            else:
                if method in ['Simplified Rankine', 'General Rankine']:
                    data_graph = pd.DataFrame({'phi': list_phi, 'Force': list_F, 'legend': legend})

                    graph_ka = data_graph[data_graph.legend == 'Active Force']
                    graph_kp = data_graph[data_graph.legend == 'Passive Force']


                else:
                    graph_ka = pd.DataFrame({'phi': list_phi, 'Active': list_Fa, 'legend': legend})
                    graph_kp = pd.DataFrame({'phi': list_phi, 'Passive':list_Fp, 'legend': legend})


#Generating Graphs
    st.subheader(method)
    if method == 'Caquot & Kerisel':
        chart_kp = (
            alt.Chart(graph_kp).mark_line().encode(
                y=alt.Y('Passive', axis=alt.Axis(title='Total passive force [kN]')),
                x='phi',
                color=alt.Color('legend')

            ).properties(
                title='Total passive force in function of friction angle'
            )
        )
        st.altair_chart(chart_kp, use_container_width=True)
        st.write(graph_kp)
    else:
        if method == 'Paik & Salgado':
            chart_Fa = (
                alt.Chart(graph_ka).mark_line().encode(
                    y=alt.Y('Active', axis=alt.Axis(title='Total Active Force [kN]')),
                    x='phi',
                    color=alt.Color('legend')

                ).properties(
                    title='Total active force in function of friction angle'
                )
            )
            st.altair_chart(chart_Fa, use_container_width=True)
            st.write(graph_ka)
        else:
            if method in ['Simplified Rankine', 'General Rankine']:
                chart_Fa = (
                    alt.Chart(graph_ka).mark_line().encode(
                        y=alt.Y('Force', axis=alt.Axis(title='Total Active Force [kN]')),
                        x='phi',
                        color=alt.Color('legend')

                    ).properties(
                        title='Total active force in function of friction angle'
                    )
                )
                st.altair_chart(chart_Fa, use_container_width=True)

                chart_kp = (
                    alt.Chart(graph_kp).mark_line().encode(
                        y=alt.Y('Force', axis=alt.Axis(title='Total passive force [kN]')),
                        x='phi',
                        color=alt.Color('legend')

                    ).properties(
                        title='Total passive force in function of friction angle'
                    )
                )
                st.altair_chart(chart_kp, use_container_width=True)
                st.write(data_graph)

            else:
                chart_Fa = (
                    alt.Chart(graph_ka).mark_line().encode(
                        y=alt.Y('Active', axis=alt.Axis(title='Total Active Force [kN]')),
                        x='phi',
                        color=alt.Color('legend')

                    ).properties(
                        title='Total active force in function of friction angle'
                    )
                )
                st.altair_chart(chart_Fa, use_container_width=True)

                chart_kp = (
                    alt.Chart(graph_kp).mark_line().encode(
                        y=alt.Y('Passive', axis=alt.Axis(title='Total passive force [kN]')),
                        x='phi',
                        color=alt.Color('legend')

                    ).properties(
                        title='Total passive force in function of friction angle'
                    )
                )
                st.altair_chart(chart_kp, use_container_width=True)
                st.write(graph_ka)
                st.write(graph_kp)

if mode == 'Stress Distribution':
    method = st.selectbox('Which method ?',
                           ['Simplified Rankine', 'General Rankine','Coulomb' , 'Caquot & Kerisel', 'Lancellotta',
                            'Paik & Salgado', 'Müller-Breslau', 'Kötter'])

    phi = st.sidebar.slider('friction angle',10,45,20)
    phi_r = dg_rad(phi)
    H = st.sidebar.slider('Heigt of the wall [m]',1,20,10)
    gamma = st.sidebar.slider('Weight of the backfill [kN/m³]',15,30,20)
    if method in [ 'General Rankine','Coulomb','Caquot & Kerisel']:

        beta = st.sidebar.slider('Inclination of the backfill (beta)',0,min(phi,30),0)
        eta = st.sidebar.slider('Inclination of the wall surface (eta)',0,30,0)
        eta_r = dg_rad(eta)
        beta_r = dg_rad(beta)

    if method in ['Coulomb' , 'Caquot & Kerisel', 'Lancellotta',
                            'Paik & Salgado', 'Müller-Breslau', 'Kötter']:
        delta_i = st.sidebar.slider('delta factor',0.1,0.75,0.5)

    list_H = []
    list_sigma = []
    legend = []

    list_d = []
    list_sigma_v = []
    list_sigma_ha = []
    list_sigma_hp = []



    if method == 'Simplified Rankine':
        ka = KASR(phi_r)
        kp = KPSR(phi_r)
        h = (H*10)+1
        for h in range(h):
            s_v = sigma_v(h/10,gamma)
            s_ha = sigma_ha(ka,s_v)
            s_hp = sigma_hp(kp,s_v)

            list_H.append(H - h/10)
            list_H.append(H - h/10)
            list_H.append(H - h/10)

            list_sigma.append(s_v)
            list_sigma.append(s_ha)
            list_sigma.append(s_hp)

            legend.append('Vertical pressure')
            legend.append('Horizontal active pressure')
            legend.append('Horizontal passive pressure')

            list_d.append(h/10)
            list_sigma_v.append(s_v)
            list_sigma_ha.append(s_ha)
            list_sigma_hp.append(s_hp)

    if method == 'General Rankine':
        ka = KAGR(phi_r,beta_r,eta_r)
        kp = KPGR(phi_r,beta_r,eta_r)
        h = (H*10)+1
        for h in range(h):
            s_v = sigma_v(h/10,gamma)
            s_ha = sigma_ha(ka,s_v)
            s_hp = sigma_hp(kp,s_v)

            list_H.append(H - h/10)
            list_H.append(H - h/10)
            list_H.append(H - h/10)

            list_sigma.append(s_v)
            list_sigma.append(s_ha)
            list_sigma.append(s_hp)

            legend.append('Vertical pressure')
            legend.append('Horizontal active pressure')
            legend.append('Horizontal passive pressure')

            list_d.append(h/10)
            list_sigma_v.append(s_v)
            list_sigma_ha.append(s_ha)
            list_sigma_hp.append(s_hp)

    if method == 'Coulomb':
        delta_r = dg_rad(phi)*delta_i
        ka = KAC(phi_r,beta_r,eta_r,delta_r)
        kp = KPC(phi_r,beta_r,eta_r,delta_r)
        h = (H*10)+1
        for h in range(h):
            s_v = sigma_v(h/10,gamma)
            s_ha = sigma_ha(ka,s_v)
            s_hp = sigma_hp(kp,s_v)

            list_H.append(H - h/10)
            list_H.append(H - h/10)
            list_H.append(H - h/10)

            list_sigma.append(s_v)
            list_sigma.append(s_ha)
            list_sigma.append(s_hp)

            legend.append('Vertical pressure')
            legend.append('Horizontal active pressure')
            legend.append('Horizontal passive pressure')

            list_d.append(h/10)
            list_sigma_v.append(s_v)
            list_sigma_ha.append(s_ha)
            list_sigma_hp.append(s_hp)

    if method == 'Caquot & Kerisel':
        delta_r = dg_rad(phi)*delta_i
        kp = KPCK(phi_r,beta_r,eta_r,delta_r)
        h = (H*10)+1
        for h in range(h):
            s_v = sigma_v(h/10,gamma)
            s_hp = sigma_hp(kp,s_v)

            list_H.append(H - h/10)
            list_H.append(H - h/10)

            list_sigma.append(s_v)
            list_sigma.append(s_hp)

            legend.append('Vertical pressure')
            legend.append('Horizontal passive pressure')

            list_d.append(h/10)
            list_sigma_v.append(s_v)
            list_sigma_hp.append(s_hp)

    if method == 'Lancellotta':
        delta_r = dg_rad(phi)*delta_i
        ka = KAL(phi_r,delta_r)
        kp = KPL(phi_r,delta_r)
        h = (H*10)+1
        for h in range(h):
            s_v = sigma_v(h/10,gamma)
            s_ha = sigma_ha(ka,s_v)
            s_hp = sigma_hp(kp,s_v)

            list_H.append(H - h/10)
            list_H.append(H - h/10)
            list_H.append(H - h/10)

            list_sigma.append(s_v)
            list_sigma.append(s_ha)
            list_sigma.append(s_hp)

            legend.append('Vertical pressure')
            legend.append('Horizontal active pressure')
            legend.append('Horizontal passive pressure')

            list_d.append(h/10)
            list_sigma_v.append(s_v)
            list_sigma_ha.append(s_ha)
            list_sigma_hp.append(s_hp)

    if method == 'Paik & Salgado':
        delta_r = dg_rad(phi)*delta_i
        ka = KAPS(phi_r,delta_r)
        h = (H*10)+1
        for h in range(h):
            s_v = sigma_v_ps(ka,gamma,H,h/10,delta_r,phi_r)
            s_ha = sigma_ha(ka,s_v)

            list_H.append(H - h/10)
            list_H.append(H - h/10)

            list_sigma.append(s_v)
            list_sigma.append(s_ha)

            legend.append('Vertical pressure')
            legend.append('Horizontal active pressure')

            list_d.append(h/10)
            list_sigma_v.append(s_v)
            list_sigma_ha.append(s_ha)

    if method == 'Müller-Breslau':
        delta_r = dg_rad(phi)*delta_i
        ka = KAMB(phi_r,delta_r)
        kp = KPMB(phi_r,delta_r)
        h = (H*10)+1
        for h in range(h):
            s_v = sigma_v(h/10,gamma)
            s_ha = sigma_ha(ka,s_v)
            s_hp = sigma_hp(kp,s_v)

            list_H.append(H - h/10)
            list_H.append(H - h/10)
            list_H.append(H - h/10)

            list_sigma.append(s_v)
            list_sigma.append(s_ha)
            list_sigma.append(s_hp)

            legend.append('Vertical pressure')
            legend.append('Horizontal active pressure')
            legend.append('Horizontal passive pressure')

            list_d.append(h/10)
            list_sigma_v.append(s_v)
            list_sigma_ha.append(s_ha)
            list_sigma_hp.append(s_hp)

    if method == 'Kötter':
        delta_r = dg_rad(phi)*delta_i
        ka = KAK(phi_r,delta_r)
        kp = KPK(phi_r,delta_r)
        h = (H*10)+1
        for h in range(h):
            s_v = sigma_v(h/10,gamma)
            s_ha = sigma_ha(ka,s_v)
            s_hp = sigma_hp(kp,s_v)

            list_H.append(H - h/10)
            list_H.append(H - h/10)
            list_H.append(H - h/10)

            list_sigma.append(s_v)
            list_sigma.append(s_ha)
            list_sigma.append(s_hp)

            legend.append('Vertical pressure')
            legend.append('Horizontal active pressure')
            legend.append('Horizontal passive pressure')

            list_d.append(h/10)
            list_sigma_v.append(s_v)
            list_sigma_ha.append(s_ha)
            list_sigma_hp.append(s_hp)



    data_graph = pd.DataFrame({'Height': list_H, 'Pressure': list_sigma, 'legend': legend})

    if method == 'Caquot & Kerisel':
        data_table = pd.DataFrame(
            {'Depth': list_d, 'Vertical pressure': list_sigma_v,
             'Horizontal passive pressure': list_sigma_hp})
        data_table = data_table.set_index('Depth')

    else:
        if method == 'Paik & Salgado':
            data_table = pd.DataFrame(
                {'Depth': list_d, 'Vertical pressure': list_sigma_v, 'Horizontal active pressure': list_sigma_ha})
            data_table = data_table.set_index('Depth')
        else:
            data_table = pd.DataFrame(
                {'Depth': list_d, 'Vertical pressure': list_sigma_v, 'Horizontal active pressure': list_sigma_ha,
                 'Horizontal passive pressure': list_sigma_hp})
            data_table = data_table.set_index('Depth')

    if method == 'Paik & Salgado':
        st.subheader(method)
        chart_pressure = (
            alt.Chart(data_graph).mark_line(order=False).encode(
                y=alt.Y('Height', axis=alt.Axis(title='Height on the wall[m]')),
                x=alt.X('Pressure', axis=alt.Axis(title='Pressure [kN/m²]')),
                color=alt.Color('legend')

            ).properties(
                title='Pressure along the wall height'
            )
        )
        st.altair_chart(chart_pressure, use_container_width=True)
        st.subheader('Tabulated results')
        st.table(data=data_table)

    else:
        st.subheader(method)
        chart_pressure = (
            alt.Chart(data_graph).mark_line().encode(
                y=alt.Y('Height', axis=alt.Axis(title='Height on the wall[m]')),
                x=alt.X('Pressure', axis=alt.Axis(title='Pressure [kN/m²]')),
                color=alt.Color('legend')

            ).properties(
                title='Pressure along the wall height'
            )
        )
        st.altair_chart(chart_pressure, use_container_width=True)
        st.subheader('Tabulated results')
        st.table(data=data_table)

if mode == 'Dynamic calculations Mononbe-Okabe':

    method = st.selectbox('Which method ?',
                           ['Classical','Total Force','adaptation by Fang and Chen','adaptation by Abodiul Ismail Lawal','adaptation by Mylonakis, Kloukinas, Papantonopoulos'])

    if method == 'Classical':
        compare = st.sidebar.selectbox('Wich parameter to compare ?',['delta','phi','beta','eta','kv'])

        if compare == 'phi':
            phi = [20,25,30,35]
            phi_r = [dg_rad(phi[0]),dg_rad(phi[1]),dg_rad(phi[2]),dg_rad(phi[3])]
        else:
            phi = st.sidebar.slider('Soil friction angle [phi]', 15, 45, 30, 1)
            phi_r = [dg_rad(phi),dg_rad(phi),dg_rad(phi),dg_rad(phi)]

        if compare == 'delta':
            delta_g = [0, 0.25 * phi, 0.5 * phi, 0.75 * phi]
            delta = [dg_rad(delta_g[0]),dg_rad(delta_g[1]),dg_rad(delta_g[2]),dg_rad(delta_g[3])]
        else:
            delta_i = st.sidebar.slider('Wall friction coefficient [delta]',0.0,1.0,0.5,0.1)
            delta = [phi_r[0]*delta_i,phi_r[1]*delta_i,phi_r[2]*delta_i,phi_r[3]*delta_i]

        if compare == 'beta':
            beta = [0,10,20,30]
            beta_r = [dg_rad(beta[0]),dg_rad(beta[1]),dg_rad(beta[2]),dg_rad(beta[3])]
        else:
            beta = st.sidebar.slider('Inclination of the backfill [beta]', 0, 30, 0)
            beta_r = [dg_rad(beta),dg_rad(beta),dg_rad(beta),dg_rad(beta)]

        if compare == 'eta':
            eta = [0,10,20,30]
            eta_r = [dg_rad(eta[0]),dg_rad(eta[1]),dg_rad(eta[2]),dg_rad(eta[3])]
        else:
            eta = st.sidebar.slider('Inclination of the wall surface [eta]', 0, 30, 0)
            eta_r = [dg_rad(eta),dg_rad(eta),dg_rad(eta),dg_rad(eta)]

        if compare == 'kv':
            kv = [0,0.1,0.2,0.4]
        else:
            Kv = st.sidebar.slider('Vertical accelarations [Kv]', 0.0, 0.5, 0.2, 0.1)
            kv = [Kv,Kv,Kv,Kv]

        list_kh = []
        list_moa = []
        list_mop = []
        legend = []
        for x in range(41):
            kh = (x/100)

            theta = [th(kh, kv[0]),th(kh, kv[1]),th(kh, kv[2]),th(kh, kv[3])]

            moa_0 = moa(phi_r[0],delta[0],beta_r[0],eta_r[0],theta[0])
            moa_1 = moa(phi_r[1],delta[1],beta_r[1],eta_r[1],theta[1])
            moa_2 = moa(phi_r[2],delta[2],beta_r[2],eta_r[2],theta[2])
            moa_3 = moa(phi_r[3],delta[3],beta_r[3],eta_r[3],theta[3])

            mop_0 = mop(phi_r[0],delta[0],beta_r[0],eta_r[0],theta[0])
            mop_1 = mop(phi_r[1],delta[1],beta_r[1],eta_r[1],theta[1])
            mop_2 = mop(phi_r[2],delta[2],beta_r[2],eta_r[2],theta[2])
            mop_3 = mop(phi_r[3],delta[3],beta_r[3],eta_r[3],theta[3])

            list_kh.append(kh)
            list_kh.append(kh)
            list_kh.append(kh)
            list_kh.append(kh)

            list_moa.append(moa_0)
            list_moa.append(moa_1)
            list_moa.append(moa_2)
            list_moa.append(moa_3)

            list_mop.append(mop_0)
            list_mop.append(mop_1)
            list_mop.append(mop_2)
            list_mop.append(mop_3)

            if compare == 'phi':
                legend.append('phi = 20°')
                legend.append('phi = 25°')
                legend.append('phi = 30°')
                legend.append('phi = 35°')
            else:
                if compare == 'delta':
                    legend.append('delta = 0')
                    legend.append('delta = 25% phi')
                    legend.append('delta = 50% phi')
                    legend.append('delta = 75% phi')
                else:
                    if compare == 'beta':
                        legend.append('beta = 0°')
                        legend.append('beta = 10°')
                        legend.append('beta = 20°')
                        legend.append('beta = 30°')
                    else:
                        if compare == 'eta':
                            legend.append('eta = 0°')
                            legend.append('eta = 10°')
                            legend.append('eta = 20°')
                            legend.append('eta = 30°')
                        else:
                            if compare == 'kv':
                                legend.append('Kv = 0')
                                legend.append('Kv = 0.1')
                                legend.append('Kv = 0.2')
                                legend.append('Kv = 0.4')

        data_graph_a = pd.DataFrame({'kh':list_kh,'moa':list_moa,'legend':legend})
        data_graph_p = pd.DataFrame({'kh':list_kh,'mop':list_mop,'legend':legend})

        chart_moa = (
            alt.Chart(data_graph_a).mark_line().encode(
                y=alt.Y('moa', axis=alt.Axis(title='Kae')),
                x=alt.X('kh', axis=alt.Axis(title='Horizontal accelaration [Kh]')),
                color=alt.Color('legend')

            ).properties(
                title='Monobe Okabe coefficient in function of horizontal accelaration'
            )
        )
        st.altair_chart(chart_moa, use_container_width=True)

        chart_mop = (
            alt.Chart(data_graph_p).mark_line().encode(
                y=alt.Y('mop', axis=alt.Axis(title='Kpe')),
                x=alt.X('kh', axis=alt.Axis(title='Horizontal accelaration [Kh]')),
                color=alt.Color('legend')

            ).properties(
                title='Monobe Okabe coefficient in function of horizontal accelaration'
            )
        )
        st.altair_chart(chart_mop, use_container_width=True)

    if method == 'Total Force':
        phi = st.sidebar.slider('Soil friction angle [phi]', 15, 45, 30, 1)
        delta_i = st.sidebar.slider('Wall friction coefficient [delta]',0.0,1.0,0.5,0.1)
        beta = st.sidebar.slider('Inclination of the backfill [beta]', 0, 30, 0)
        eta = st.sidebar.slider('Inclination of the wall surface [eta]', 0, 30, 0)
        Kv = st.sidebar.slider('Vertical accelarations [Kv]', 0.0, 0.5, 0.2, 0.1)
        Kh = st.sidebar.slider('Horizontal accelarations [Kh]', 0.0, 0.5, 0.2, 0.1)
        H = st.sidebar.slider('Height of the wall [H]', 0, 20, 5,)
        gamma = st.sidebar.slider('Weight of the backfill [gamma]', 15, 40, 20,)

        phi_r = dg_rad(phi)
        delta = phi_r * delta_i
        beta_r = dg_rad(beta)
        eta_r = dg_rad(eta)
        theta = th(Kh,Kv)

        Kae = moa(phi_r,delta,beta_r,eta_r,theta)
        Pae = Pae(gamma,H,Kv,Kae)
        ka = KAC(phi_r,beta_r,eta_r,delta)
        Pa = FKA(ka,H,gamma)

        Pad = Pae - Pa
        L = L(Pae,Pad,H)

        st.text('The total force on the wall:')
        st.write(Pae,'kN')
        st.write('The static component:')
        st.write(Pa,'kN')
        st.write('Extra force caused by the earthquake:')
        st.write(Pae-Pa,'kN')
        st.write('Aplied at a height of:')
        st.write(L,'m')

    if method == 'adaptation by Fang and Chen':
        units = st.sidebar.selectbox('Wich mode',({'coefficient','Total Force','Dimensionless'}))
        phi = st.sidebar.slider('Soil friction angle [phi]', 15, 45, 30, 1)
        phi_r = dg_rad(phi)
        delta_i = st.sidebar.slider('Wall friction coefficient [delta]',0.0,1.0,0.5,0.1)
        delta_r = phi_r*delta_i
        beta = st.sidebar.slider('Inclination of the backfill [beta]', 0, 30, 0)
        beta_r = dg_rad(beta)
        eta = st.sidebar.slider('Inclination of the wall surface [eta]', 0, 30, 0)
        eta_r = dg_rad(eta)
        gamma = st.sidebar.slider('Weight of the backfill [gamma]', 15, 45, 20)
        H = st.sidebar.slider('Heigth of the wall [H]', 2, 20, 5)
        list_mo = []
        list_kh = []
        list_kh_c = []
        legend = []
        legend_c = []
        list_N = []
        kv_u = 0.2
        kv_d = -0.2
        kv_n = 0


        for x in range(81):
            kh = (x/100)-0.4
            theta_u = th(kh,kv_u)
            theta_d = th(kh,kv_d)
            theta_n = th(kh,kv_n)

            mo_u = moa(phi_r,delta_r,beta_r,eta_r,theta_u)
            mo_d = moa(phi_r,delta_r,beta_r,eta_r,theta_d)
            mo_n = moa(phi_r,delta_r,beta_r,eta_r,theta_n)

            F_u = Pae(gamma,H,kv_u,mo_u)
            F_d = Pae(gamma,H,kv_d,mo_d)
            F_n = Pae(gamma,H,kv_n,mo_n)

            K_u = Pae(gamma,H,kv_u,mo_u)*2/(gamma*H**2)
            K_d = Pae(gamma,H,kv_d,mo_d)*2/(gamma*H**2)
            K_n = Pae(gamma,H,kv_n,mo_n)*2/(gamma*H**2)

            if units == 'coefficient':
                list_mo.append(mo_u)
                list_mo.append(mo_d)
                list_mo.append(mo_n)
            else:
                if units == 'Total Force':
                    list_mo.append(F_u)
                    list_mo.append(F_d)
                    list_mo.append(F_n)
                else:
                    list_mo.append(K_u)
                    list_mo.append(K_d)
                    list_mo.append(K_n)

            list_kh.append(kh)
            list_kh.append(kh)
            list_kh.append(kh)

            legend.append('kv = 0.2')
            legend.append('kv = -0.2')
            legend.append('kv = 0')

            for x in range(41):
                kh = (x/100)
                theta_cu = th(kh, kh / 2)
                theta_cd = th(kh, -kh / 2)

                mo_cu = moa(phi_r, delta_r, beta_r, eta_r, theta_cu)
                mo_cd = moa(phi_r, delta_r, beta_r, eta_r, theta_cd)

                F_cu = Pae(gamma, H, kh / 2, mo_cu)
                F_cd = Pae(gamma, H, -kh / 2, mo_cd)

                N = compare(F_cu, F_cd)
                if N == 0:
                    error = True
                else:
                    list_N.append(N)
                    list_kh_c.append(kh)
                    legend_c.append('(F_d-F_u)/F_u')



        data_graph = pd.DataFrame({'kh':list_kh,'mo':list_mo,'legend':legend})
        data_compare = pd.DataFrame({'kh':list_kh_c,'Compare':list_N,'legend':legend_c})

        chart_moa = (
            alt.Chart(data_graph).mark_line().encode(
                y=alt.Y('mo', axis=alt.Axis(title='Kae')),
                x=alt.X('kh', axis=alt.Axis(title='Horizontal accelaration [Kh]')),
                color=alt.Color('legend')

            ).properties(
                title='Monobe Okabe comparing directions'
            )
        )

        st.altair_chart(chart_moa, use_container_width=True)
        chart_c = (
            alt.Chart(data_compare).mark_line().encode(
                y=alt.Y('Compare', axis=alt.Axis(title='(F_d-F_u)/F_u')),
                x=alt.X('kh', axis=alt.Axis(title='Horizontal accelaration [Kh]')),
                color=alt.Color('legend')

            ).properties(
                title='Monobe Okabe comparing directions'
            )
        )

        st.altair_chart(chart_c, use_container_width=True)


    if method == 'adaptation by Abodiul Ismail Lawal':
        compare = st.sidebar.selectbox('Wich parameter to compare ?',['delta','phi','kv','kh'])

        if compare == 'phi':
            phi = [20,25,30,35]
            phi_r = [dg_rad(phi[0]),dg_rad(phi[1]),dg_rad(phi[2]),dg_rad(phi[3])]
        else:
            phi = st.sidebar.slider('Soil friction angle [phi]', 15, 45, 30, 1)
            phi_r = [dg_rad(phi),dg_rad(phi),dg_rad(phi),dg_rad(phi)]

        if compare == 'delta':
            delta_g = [0, 0.25 * phi, 0.5 * phi, 0.75 * phi]
            delta = [dg_rad(delta_g[0]),dg_rad(delta_g[1]),dg_rad(delta_g[2]),dg_rad(delta_g[3])]
        else:
            delta_i = st.sidebar.slider('Wall friction coefficient [delta]',0.0,1.0,0.5,0.1)
            delta = [phi_r[0]*delta_i,phi_r[1]*delta_i,phi_r[2]*delta_i,phi_r[3]*delta_i]

        if compare == 'kv':
            kv = [0,0.1,0.2,0.4]
        else:
            Kv = st.sidebar.slider('Vertical accelarations [Kv]', 0.0, 0.5, 0.2, 0.1)
            kv = [Kv,Kv,Kv,Kv]
        if compare == 'kh':
            kh = [0,0.1,0.2,0.4]
        else:
            Kh= st.sidebar.slider('Horizontal accelarations [Kh]', 0.0, 0.5, 0.2, 0.1)
            kh = [Kh,Kh,Kh,Kh]


        gamma = st.sidebar.slider('Weight of the backfill [gamma]', 15, 45, 20)
        H = st.sidebar.slider('Heigth of the wall [H]', 2, 20, 5)

        list_L = []
        list_SV = []
        list_SH = []
        legend = []
        theta = [th(kh[0], kv[0]), th(kh[1], kv[1]), th(kh[2], kv[2]), th(kh[3], kv[3])]
        kp = [KPSR(phi_r[0]), KPSR(phi_r[1]), KPSR(phi_r[2]), KPSR(phi_r[3])]
        a = [a(delta[0], theta[0], phi_r[0]), a(delta[1], theta[1], phi_r[1]), a(delta[2], theta[2], phi_r[2]),
             a(delta[3], theta[3], phi_r[3])]
        b = [b(delta[0], theta[0], phi_r[0]), b(delta[1], theta[1], phi_r[1]), b(delta[2], theta[2], phi_r[2]),
             b(delta[3], theta[3], phi_r[3])]
        C = [C(delta[0], theta[0], phi_r[0]), C(delta[1], theta[1], phi_r[1]), C(delta[2], theta[2], phi_r[2]),
             C(delta[3], theta[3], phi_r[3])]
        alpha = [alpha(a[0], b[0], C[0]), alpha(a[1], b[1], C[1]), alpha(a[2], b[2], C[2]), alpha(a[3], b[3], C[3])]
        A = [A(phi_r[0], alpha[0], delta[0]), A(phi_r[1], alpha[1], delta[1]), A(phi_r[2], alpha[2], delta[2]),
             A(phi_r[3], alpha[3], delta[3])]
        B = [B(phi_r[0], alpha[0], kh[0], kv[0]), B(phi_r[1], alpha[1], kh[1], kv[1]),
             B(phi_r[2], alpha[2], kh[2], kv[2]), B(phi_r[3], alpha[3], kh[3], kv[3])]
        L = H
        h = (H*10)
        H_AIL_0 = H_AIL(H,phi_r[0],alpha[0],delta[0],kp[0])
        H_AIL_1 = H_AIL(H,phi_r[1],alpha[1],delta[1],kp[1])
        H_AIL_2 = H_AIL(H,phi_r[2],alpha[2],delta[2],kp[2])
        H_AIL_3 = H_AIL(H,phi_r[3],alpha[3],delta[3],kp[3])


        P_AIL_0 = P_AIL(gamma, H, kv[0], delta[0], alpha[0], phi_r[0], theta[0])
        P_AIL_1 = P_AIL(gamma, H, kv[1], delta[1], alpha[1], phi_r[1], theta[1])
        P_AIL_2 = P_AIL(gamma, H, kv[2], delta[2], alpha[2], phi_r[2], theta[2])
        P_AIL_3 = P_AIL(gamma, H, kv[3], delta[3], alpha[3], phi_r[3], theta[3])

        for l in range(h):
            L = H -(l/10)

            SV_AIL_0 = SV_AIL(A[0], B[0], gamma, kp[0], L, H)
            SV_AIL_1 = SV_AIL(A[1], B[1], gamma, kp[1], L, H)
            SV_AIL_2 = SV_AIL(A[2], B[2], gamma, kp[2], L, H)
            SV_AIL_3 = SV_AIL(A[3], B[3], gamma, kp[3], L, H)

            SH_AIL_0 = SH_AIL(SV_AIL_0,kp[0])
            SH_AIL_1 = SH_AIL(SV_AIL_1,kp[1])
            SH_AIL_2 = SH_AIL(SV_AIL_2,kp[2])
            SH_AIL_3 = SH_AIL(SV_AIL_3,kp[3])

            list_L.append(L)
            list_L.append(L)
            list_L.append(L)
            list_L.append(L)

            list_SV.append(SV_AIL_0)
            list_SV.append(SV_AIL_1)
            list_SV.append(SV_AIL_2)
            list_SV.append(SV_AIL_3)

            list_SH.append(SH_AIL_0)
            list_SH.append(SH_AIL_1)
            list_SH.append(SH_AIL_2)
            list_SH.append(SH_AIL_3)

            if compare == 'phi':
                legend.append('phi = 20°')
                legend.append('phi = 25°')
                legend.append('phi = 30°')
                legend.append('phi = 35°')
            else:
                if compare == 'delta':
                    legend.append('delta = 0')
                    legend.append('delta = 25% phi')
                    legend.append('delta = 50% phi')
                    legend.append('delta = 75% phi')
                else:
                            if compare == 'kv':
                                legend.append('Kv = 0')
                                legend.append('Kv = 0.1')
                                legend.append('Kv = 0.2')
                                legend.append('Kv = 0.4')
                            else:
                                if compare == 'kh':
                                    legend.append('Kh = 0')
                                    legend.append('Kh = 0.1')
                                    legend.append('Kh = 0.2')
                                    legend.append('Kh = 0.4')


        data_graph_V = pd.DataFrame({'L':list_L,'SV_AIL':list_SV,'legend':legend})
        data_graph_H = pd.DataFrame({'L':list_L,'SH_AIL':list_SH,'legend':legend})

        chart_AIL_V = (
            alt.Chart(data_graph_V).mark_line(order = False).encode(
                y=alt.Y('L', axis=alt.Axis(title='Height on the wall')),
                x=alt.X('SV_AIL', axis=alt.Axis(title='Vertical pressure on wall')),
                color=alt.Color('legend')

            ).properties(
                title='Vertical pressure per wall height by Abiodun Ismail LAWAL'
            )
        )
        st.altair_chart(chart_AIL_V, use_container_width=True)

        chart_AIL_H = (
            alt.Chart(data_graph_H).mark_line(order = False).encode(
                y=alt.Y('L', axis=alt.Axis(title='Height on the wall')),
                x=alt.X('SH_AIL', axis=alt.Axis(title='Horizontal pressure on wall')),
                color=alt.Color('legend')

            ).properties(
                title='Horizontal pressure per wall height by Abiodun Ismail LAWAL'
            )
        )
        st.altair_chart(chart_AIL_H, use_container_width=True)
        st.write('case 1 total force =',P_AIL_0,'kN','at a height of',H_AIL_0,'m')
        st.write('case 2 total force =', P_AIL_1, 'kN', 'at a height of', H_AIL_1, 'm')
        st.write('case 3 total force =', P_AIL_2, 'kN', 'at a height of', H_AIL_2, 'm')
        st.write('case 4 total force =', P_AIL_3, 'kN', 'at a height of', H_AIL_3, 'm')

    if method == 'adaptation by Mylonakis, Kloukinas, Papantonopoulos':
        compare = st.sidebar.selectbox('Wich parameter to compare ?',['delta','phi','beta','eta','kv'])

        if compare == 'phi':
            phi = [20,25,30,35]
            phi_r = [dg_rad(phi[0]),dg_rad(phi[1]),dg_rad(phi[2]),dg_rad(phi[3])]
        else:
            phi = st.sidebar.slider('Soil friction angle [phi]', 15, 45, 30, 1)
            phi_r = [dg_rad(phi),dg_rad(phi),dg_rad(phi),dg_rad(phi)]

        if compare == 'delta':
            delta_g = [0, 0.25 * phi, 0.5 * phi, 0.75 * phi]
            delta = [dg_rad(delta_g[0]),dg_rad(delta_g[1]),dg_rad(delta_g[2]),dg_rad(delta_g[3])]
        else:
            delta_i = st.sidebar.slider('Wall friction coefficient [delta]',0.0,1.0,0.5,0.1)
            delta = [phi_r[0]*delta_i,phi_r[1]*delta_i,phi_r[2]*delta_i,phi_r[3]*delta_i]

        if compare == 'beta':
            beta = [0,10,20,30]
            beta_r = [dg_rad(beta[0]),dg_rad(beta[1]),dg_rad(beta[2]),dg_rad(beta[3])]
        else:
            beta = st.sidebar.slider('Inclination of the backfill [beta]', 0, 30, 0)
            beta_r = [dg_rad(beta),dg_rad(beta),dg_rad(beta),dg_rad(beta)]

        if compare == 'eta':
            eta = [0,10,20,30]
            eta_r = [dg_rad(eta[0]),dg_rad(eta[1]),dg_rad(eta[2]),dg_rad(eta[3])]
        else:
            eta = st.sidebar.slider('Inclination of the wall surface [eta]', 0, 30, 0)
            eta_r = [dg_rad(eta),dg_rad(eta),dg_rad(eta),dg_rad(eta)]

        if compare == 'kv':
            kv = [0,0.1,0.2,0.4]
        else:
            Kv = st.sidebar.slider('Vertical accelarations [Kv]', 0.0, 0.5, 0.2, 0.1)
            kv = [Kv,Kv,Kv,Kv]

        list_kh = []
        list_moa = []
        list_mop = []
        legend = []

        d1 = [d1(beta_r[0],phi_r[0]),d1(beta_r[1],phi_r[1]),d1(beta_r[2],phi_r[2]),d1(beta_r[3],phi_r[3])]
        d2 = [d2(delta[0],phi_r[0]),d2(delta[1],phi_r[1]),d2(delta[2],phi_r[2]),d2(delta[3],phi_r[3])]
        for x in range(41):
            kh = (x/100)

            theta_0 = th(kh, kv[0])
            theta_1 = th(kh, kv[1])
            theta_2 = th(kh, kv[2])
            theta_3 = th(kh, kv[3])

            d1_s_0 = d1_s(beta_r[0],phi_r[0],theta_0)
            d1_s_1 = d1_s(beta_r[1],phi_r[1],theta_1)
            d1_s_2 = d1_s(beta_r[2],phi_r[2],theta_2)
            d1_s_3 = d1_s(beta_r[3],phi_r[3],theta_3)

            theta_EA_0 = theta_EA(d1_s_0,d2[0],delta[0],beta_r[0],eta_r[0],theta_0)
            theta_EA_1 = theta_EA(d1_s_1,d2[1],delta[1],beta_r[1],eta_r[1],theta_1)
            theta_EA_2 = theta_EA(d1_s_2,d2[2],delta[2],beta_r[2],eta_r[2],theta_2)
            theta_EA_3 = theta_EA(d1_s_3,d2[3],delta[3],beta_r[3],eta_r[3],theta_3)

            theta_EP_0 = theta_EP(d1_s_0,d2[0],delta[0],beta_r[0],eta_r[0],theta_0)
            theta_EP_1 = theta_EP(d1_s_1,d2[1],delta[1],beta_r[1],eta_r[1],theta_1)
            theta_EP_2 = theta_EP(d1_s_2,d2[2],delta[2],beta_r[2],eta_r[2],theta_2)
            theta_EP_3 = theta_EP(d1_s_3,d2[3],delta[3],beta_r[3],eta_r[3],theta_3)

            moa_0 = KEA_MKP(eta_r[0],beta_r[0],theta_0,phi_r[0],delta[0],d1_s_0,d2[0],theta_EA_0)
            moa_1 = KEA_MKP(eta_r[1],beta_r[1],theta_1,phi_r[1],delta[1],d1_s_1,d2[1],theta_EA_1)
            moa_2 = KEA_MKP(eta_r[2],beta_r[2],theta_2,phi_r[2],delta[2],d1_s_2,d2[2],theta_EA_2)
            moa_3 = KEA_MKP(eta_r[3],beta_r[3],theta_3,phi_r[3],delta[3],d1_s_3,d2[3],theta_EA_3)

            mop_0 = KEP_MKP(eta_r[0],beta_r[0],theta_0,phi_r[0],delta[0],d1_s_0,d2[0],theta_EP_0)
            mop_1 = KEP_MKP(eta_r[1],beta_r[1],theta_1,phi_r[1],delta[1],d1_s_1,d2[1],theta_EP_1)
            mop_2 = KEP_MKP(eta_r[2],beta_r[2],theta_2,phi_r[2],delta[2],d1_s_2,d2[2],theta_EP_2)
            mop_3 = KEP_MKP(eta_r[3],beta_r[3],theta_3,phi_r[3],delta[3],d1_s_3,d2[3],theta_EP_3)

            list_kh.append(kh)
            list_kh.append(kh)
            list_kh.append(kh)
            list_kh.append(kh)

            list_moa.append(moa_0)
            list_moa.append(moa_1)
            list_moa.append(moa_2)
            list_moa.append(moa_3)

            list_mop.append(mop_0)
            list_mop.append(mop_1)
            list_mop.append(mop_2)
            list_mop.append(mop_3)

            if compare == 'phi':
                legend.append('phi = 20°')
                legend.append('phi = 25°')
                legend.append('phi = 30°')
                legend.append('phi = 35°')
            else:
                if compare == 'delta':
                    legend.append('delta = 0')
                    legend.append('delta = 25% phi')
                    legend.append('delta = 50% phi')
                    legend.append('delta = 75% phi')
                else:
                    if compare == 'beta':
                        legend.append('beta = 0°')
                        legend.append('beta = 10°')
                        legend.append('beta = 20°')
                        legend.append('beta = 30°')
                    else:
                        if compare == 'eta':
                            legend.append('eta = 0°')
                            legend.append('eta = 10°')
                            legend.append('eta = 20°')
                            legend.append('eta = 30°')
                        else:
                            if compare == 'kv':
                                legend.append('Kv = 0')
                                legend.append('Kv = 0.1')
                                legend.append('Kv = 0.2')
                                legend.append('Kv = 0.4')

        data_graph_a = pd.DataFrame({'kh':list_kh,'moa':list_moa,'legend':legend})
        data_graph_p = pd.DataFrame({'kh':list_kh,'mop':list_mop,'legend':legend})

        chart_moa = (
            alt.Chart(data_graph_a).mark_line().encode(
                y=alt.Y('moa', axis=alt.Axis(title='Kae')),
                x=alt.X('kh', axis=alt.Axis(title='Horizontal accelaration [Kh]')),
                color=alt.Color('legend')

            ).properties(
                title='adaptation by Mylonakis, Kloukinas, Papantonopoulos active'
            )
        )
        st.altair_chart(chart_moa, use_container_width=True)

        chart_mop = (
            alt.Chart(data_graph_p).mark_line().encode(
                y=alt.Y('mop', axis=alt.Axis(title='Kpe')),
                x=alt.X('kh', axis=alt.Axis(title='Horizontal accelaration [Kh]')),
                color=alt.Color('legend')

            ).properties(
                title='adaptation by Mylonakis, Kloukinas, Papantonopoulos passive'
            )
        )
        st.altair_chart(chart_mop, use_container_width=True)

if mode == 'Wave propagation':
    u_g0 = st.sidebar.slider('Ground acceleration [m/s²]',0.0,10.0,1.0,0.1)
    freq = st.sidebar.slider('Frequentie [Hz]',0.1,10.0,2.0,0.01)
    H = st.sidebar.slider('Height [m]',1,20,5,)
    V = st.sidebar.slider('Veloscity [m/s]',0,20,5)
    beta = st.sidebar.slider('Ground damping ratio',0.0,1.0,0.05,0.005)
    t = st.sidebar.slider('Time',0.0,1.0,0.0,0.001)
    L = st.sidebar.slider('Maximum length [m]',5,100,5)
    wave = waveprob(u_g0,freq,H,V,beta,t,L)
    chart_wave = (
        alt.Chart(wave).mark_line(order = False).encode(
            y=alt.Y('Depth', axis=alt.Axis(title='Depth [m]')),
            x=alt.X('Displacement', axis=alt.Axis(title='Displacements [m]')),
            color=alt.Color('legend')

        ).properties(
            title='1D - Wave propigations'
        )
    )
    st.altair_chart(chart_wave, use_container_width=True)




