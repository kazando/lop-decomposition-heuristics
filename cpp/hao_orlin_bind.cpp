#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <lemon/list_graph.h>
#include <lemon/hao_orlin.h>

#include <vector>
#include <tuple>
#include <set>

namespace py = pybind11;
using namespace lemon;

// ================================
// 最小カット値のみ
// ================================
double min_cut(
    int n,
    const std::vector<std::tuple<int,int,double>>& edges
) {
    ListDigraph g;
    std::vector<ListDigraph::Node> nodes(n);

    for (int i = 0; i < n; ++i)
        nodes[i] = g.addNode();

    ListDigraph::ArcMap<double> cap(g);

    for (auto &[u, v, c] : edges) {
        auto a = g.addArc(nodes[u], nodes[v]);
        cap[a] = c;
    }

    HaoOrlin<ListDigraph, ListDigraph::ArcMap<double>> ho(g, cap);
    ho.run();

    return ho.minCutValue();
}


// ================================
// カット値 + 分割 (S, T)
// ================================
py::dict min_cut_with_partition(
    int n,
    const std::vector<std::tuple<int,int,double>>& edges
) {
    ListDigraph g;
    std::vector<ListDigraph::Node> nodes(n);

    for (int i = 0; i < n; ++i)
        nodes[i] = g.addNode();

    ListDigraph::ArcMap<double> cap(g);

    for (auto &[u, v, c] : edges) {
        auto a = g.addArc(nodes[u], nodes[v]);
        cap[a] = c;
    }

    HaoOrlin<ListDigraph, ListDigraph::ArcMap<double>> ho(g, cap);
    ho.run();

    double cut_value = ho.minCutValue();

    // ✅ cut map を取得
    ListDigraph::NodeMap<bool> cut(g);
    ho.minCutMap(cut);

    std::set<int> S;
    std::set<int> T;

    for (int i = 0; i < n; ++i) {
        if (cut[nodes[i]]) {
            S.insert(i);
        } else {
            T.insert(i);
        }
    }

    py::dict result;
    result["value"] = cut_value;
    result["S"] = S;
    result["T"] = T;

    return result;
}


// ================================
// Pythonモジュール定義
// ================================
PYBIND11_MODULE(hao_orlin_cpp, m) {
    m.doc() = "Hao-Orlin minimum cut (LEMON) Python binding";

    m.def("min_cut", &min_cut,
          "Compute global minimum cut value");

    m.def("min_cut_with_partition", &min_cut_with_partition,
          "Compute min cut and return partition");
}