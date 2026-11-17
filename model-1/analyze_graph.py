
# -*- coding: utf-8 -*-
"""
Универсальный разбор и сравнение мер центральности.
Форматы: .gml (Newman/football), .edges (networkrepository), .mtx (Matrix Market)
Запуск: python analyze_graph.py <файл_графа>
Выход:  *_centralities.csv, матрица Спирмена, топ-10, диаграммы рассеяния.
"""
import sys, os
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

def load_graph(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".gml":
        with open(path, "rb") as f:
            raw = f.read()
        # в файлах Newman перед GML бывает строка с "#"
        text = raw.decode("utf-8", errors="ignore")
        if text.lstrip().startswith("#"):
            lines = text.split("\n")
            if lines and lines[0].lstrip().startswith("#"):
                lines = lines[1:]
                text = "\n".join(lines)
            # вторая строка-комментарий тоже возможна
            if text.lstrip().startswith("#"):
                text = text.split("\n", 1)[1]
        G = nx.parse_gml(text.split("\n"))
        # убрать дубликаты рёбер на всякий случай
        G = nx.Graph(G)
        return G, "gml"
    if ext == ".edges":
        df = pd.read_csv(path, sep=r"\s+", header=None, usecols=[0, 1],
                         names=["u", "v"], comment="%")
        G = nx.Graph()
        G.add_edges_from(map(tuple, df[["u", "v"]].values))
        return G, "edges"
    if ext == ".mtx":
        rows = []
        with open(path) as f:
            for line in f:
                if line.startswith("%") or not line.strip():
                    continue
                parts = line.split()
                if len(parts) == 3:
                    rows.append((int(parts[0]), int(parts[1])))
                elif len(parts) == 2:
                    rows.append((int(parts[0]), int(parts[1])))
        G = nx.Graph()
        G.add_edges_from((u, v) for u, v in rows if u != v)
        return G, "mtx"
    raise ValueError(f"Неизвестный формат: {ext}")

def main(path):
    G, fmt = load_graph(path)
    n0, m0 = G.number_of_nodes(), G.number_of_edges()
    print(f"Файл: {os.path.basename(path)} ({fmt}); узлов: {n0}, рёбер: {m0}")

    # крупнейшая компонента
    if not nx.is_connected(G):
        comps = sorted(nx.connected_components(G), key=len, reverse=True)
        print(f"Компонент связности: {len(comps)}; работаем на крупнейшей ({len(comps[0])} узлов)")
        G = G.subgraph(comps[0]).copy()

    # центральности
    deg = dict(G.degree())
    bet = nx.betweenness_centrality(G, normalized=True)
    eig = nx.eigenvector_centrality_numpy(G)
    pr  = nx.pagerank(G, alpha=0.85)
    core = nx.core_number(G)

    df = pd.DataFrame({"degree": deg, "betweenness": bet,
                       "eigenvector": eig, "pagerank": pr, "k-core": core})
    df.index.name = "node"
    base = os.path.splitext(os.path.basename(path))[0]
    df.to_csv(f"{base}_centralities.csv")

    print(f"Плотность: {2*G.number_of_edges()/(len(G)*(len(G)-1)):.4f}, "
          f"ср. степень: {2*G.number_of_edges()/len(G):.2f}, "
          f"кластеризация: {nx.average_clustering(G):.3f}")

    # Спирмен между мерами
    measures = ["degree", "betweenness", "eigenvector", "pagerank", "k-core"]
    R = pd.DataFrame(index=measures, columns=measures, dtype=float)
    for i, a in enumerate(measures):
        for b in measures[i:]:
            r = spearmanr(df[a], df[b]).statistic
            R.loc[a, b] = R.loc[b, a] = r
    print("\nСпирмен между мерами:")
    print(R.round(2).to_string())

    # топ-10
    print("\nТоп-10 по каждой мере:")
    for m in measures:
        top = df[m].sort_values(ascending=False).head(10)
        print(f"  {m:>12}: " + ", ".join(f"{k}({v:.3g})" for k, v in top.items()))

    # графики
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    for ax, (m1, m2) in zip(axes, [("degree", "betweenness"),
                                    ("degree", "eigenvector")]):
        ax.scatter(df[m1], df[m2], s=22, alpha=0.6)
        ax.set_xscale("log"); ax.set_yscale("log")
        ax.set_xlabel(m1); ax.set_ylabel(m2)
        ax.set_title(f"{base}: {m1} vs {m2}")
    fig.tight_layout()
    fig.savefig(f"{base}_scatter.png", dpi=140)
    print(f"\nСохранено: {base}_centralities.csv, {base}_scatter.png")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "misc-football.mtx")
