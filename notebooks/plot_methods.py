
import matplotlib.pyplot as plt 
import networkx as nx
import pandas as pd 
import numpy as np
import math


# %% General stats

def datasets_stats(tables):
    general_table = {"Name": [], "Size": []}
    for name, path in tables.items():
        general_table["Name"].append(name)
        general_table["Size"].append(len(pd.read_csv(path)))

    return pd.DataFrame(general_table)


def load_template(template_path):
    return pd.read_csv(template_path)


# %% Event statistics

def get_length_dist(df):
    event_seq = df["Event ID"]
    event_length = event_seq.apply(lambda x: len(eval(x)))
    values = list(pd.unique(event_length))
    heights = np.zeros(len(values))

    for e in event_length:
        heights[values.index(e)] += 1
    values = np.array(values)
    idx = np.argsort(values)

    return values[idx], heights[idx]

    
def unique_elements(df):
    bag_words = {}
    event_seq = df["Event ID"]
    for seq in event_seq:
        for elem in eval(seq):
            bag_words[elem] = bag_words.get(elem, 0) + 1

    return bag_words


def get_unique_elements(df):
    unique = unique_elements(df)

    idx = np.flip(np.argsort(list(unique.values())))
    values = np.array(list(unique.keys()))[idx]
    heights = np.array(list(unique.values()))[idx]

    return values, heights


def plot_events_length(tables):
    fig, axs = plt.subplots(1, figsize=(10, 5))
    fig.suptitle("Event sequence length", fontsize=20)

    for label, path in tables.items():
        df = pd.read_csv(path)

        values_length, heights_length = get_length_dist(df)
        axs.bar(values_length, heights_length, alpha=0.4)
        axs.plot(values_length, heights_length, label=label)

    axs.grid()
    axs.legend()

    axs.set_xlabel("Length event sequence", fontsize=14)
    axs.set_ylabel("Amount of event sequences", fontsize=14)


def plot_unique_events(tables):
    rows = math.ceil(len(tables) / 2)
    fig, axs = plt.subplots(rows, 2, figsize=(14, 10))
    fig.suptitle("Event ID distribution", fontsize=20)

    for i, (name, path) in enumerate(tables.items()):
        row = math.floor(i / rows)
        column = i % rows
        axs[row, column].set_title(name, fontsize=18)
    
        df = pd.read_csv(path)
        values_unique, heights_unique = get_unique_elements(df)

        axs[row, column].pie(heights_unique, labels=values_unique, autopct="%1.1f%%")

# %% Time difference

def plot_violin(df, ax, do_xlabel=True, do_ylabel=True):
    time_diff = df["Time Diff"].apply(lambda x: eval(x))
    event_seqs = df["Event ID"].apply(lambda x: eval(x)[1:])

    stats = {}
    for events, times in zip(event_seqs, time_diff):
        for event, time in zip(events, times):
            if event not in stats.keys():
                stats[event] = []
            stats[event].append(time)


    values = list(stats.keys())
    times = list(stats.values())

    ax.violinplot(times)
    ax.set_xticks(range(1, len(values) + 1), np.array(values).astype(str))
    ax.grid()
    if do_xlabel:
        ax.set_xlabel("Event ID", fontsize=17)
    if do_ylabel:
        ax.set_ylabel("Time range", fontsize=17)


def plot_time_diff(tables):
    rows = math.ceil(len(tables) / 2)
    _, axs = plt.subplots(rows, 2, figsize=(14, 10))

    for i, (name, path) in enumerate(tables.items()):
        row = math.floor(i / rows)
        column = i % rows
        axs[row, column].set_title(name, fontsize=18)

        plot_violin(
            df=pd.read_csv(path), 
            ax=axs[row, column],
            do_xlabel=row == (rows - 1),
            do_ylabel=column == 0
        )


# %% Level log distribution

def plot_pie(df, ax):
    levels_seq = df["Level"].apply(lambda x: eval(x))

    stats = {}
    for levels in levels_seq:
        for level in levels:
            stats[level] = stats.get(level, 0) + 1


    levels = list(stats.keys())
    values = list(stats.values())

    ax.pie(values, labels=levels, autopct="%1.1f%%")


def plot_level_dist(tables):
    rows = math.ceil(len(tables) / 2)
    _, axs = plt.subplots(rows, 2, figsize=(14, 10))
    
    for i, (name, path) in enumerate(tables.items()):
        row = math.floor(i / rows)
        column = i % rows
        axs[row, column].set_title(name, fontsize=18)
        plot_pie(df=pd.read_csv(path), ax=axs[row, column])


# %% Execturion plot graph
 
def plot_execution_graph(tables):
    for i, (name, path) in enumerate(tables.items()):
        df = pd.read_csv(path)
        content_seqs = df["Content"].apply(lambda x: eval(x))

        G = nx.DiGraph()
        for content_seq in content_seqs:
            for c1, c2 in zip(content_seq[:-1], content_seq[1:]):
                G.add_edge(c1, c2)

        plt.figure(i, figsize=(20, 5))
        plt.title(name, fontsize=18)
        nx.draw(G, with_labels = True)