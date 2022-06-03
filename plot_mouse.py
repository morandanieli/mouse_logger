#!/usr/bin/env python
# coding: utf-8
import os

import pandas as pd
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mtl


def get_data(session_id):
    # Read sqlite query results into a pandas DataFrame
    con = sqlite3.connect("/Users/moran/PycharmProjects/keylogger/db/logger.db")
    df = pd.read_sql_query("SELECT * from moves where session_id='{}'".format(session_id), con)

    # Verify that result of SQL query is stored in the dataframe
    con.close()
    return df


def handle_session(df):
    df.sort_values('timestamp', inplace=True)
    moves = df[df['event_type'] == 'move']
    moves.reset_index(drop=True, inplace=True)
    clicks = df[df['event_type'] == 'click']
    clicks.reset_index(drop=True, inplace=True)
    # calc dist
    dx = moves["x"].iloc[1:].values - moves["x"].iloc[0:-1].values
    dy = moves["y"].iloc[1:].values - moves["y"].iloc[0:-1].values
    moves['dist'] = np.append([0], np.sqrt(np.power(dx, 2) + np.power(dy, 2)))
    # calc time change 
    dt = moves["timestamp"].iloc[1:].values - moves["timestamp"].iloc[0:-1].values
    moves['dt'] = np.append([0], dt)
    print(moves['dt'])
    moves['speed'] = moves['dist'] / moves['dt']
    moves['speed'].fillna(0, inplace=True)
    
    moves['speed_cat'] = pd.cut(moves['speed'], bins=np.arange(-1,20), labels=np.arange(1,21))

    return moves, clicks


def generate_fig(moves, clicks, output_filename):
    plt.rcParams['axes.facecolor'] = 'black'    
    fig, ax = plt.subplots( nrows=1, ncols=1 )   
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)    

    prev_val = None
    rows = []
    cmap = mtl.cm.get_cmap('Reds_r')
    norm = mtl.colors.Normalize(vmin=1, vmax=20)

    for index, row in moves.iterrows():
        if prev_val == row['speed_cat'] or prev_val == None:
            rows.append(index)
        else:
            rows.append(index)
            plt.plot(moves.loc[rows]['x'], moves.loc[rows]['y'], c=cmap(norm(prev_val)))
            rows = [index]
        prev_val = row['speed_cat']

    plt.scatter(clicks['x'], clicks['y'], s=200)
    
    fig.savefig(output_filename, bbox_inches='tight')
    plt.close(fig) 
    

def generate_image(session_id, output_filename):
    df = get_data(session_id=session_id)
    moves, clicks = handle_session(df)
    generate_fig(moves, clicks, output_filename)


