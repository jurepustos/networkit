/*
 * TopologicalSort.cpp
 *
 *  Created on: 22.11.2021
 *      Author: Fabian Brandt-Tumescheit
 */
#include <networkit/graph/TopologicalSort.hpp>

namespace NetworKit {

TopologicalSort::TopologicalSort(
    const Graph &G,
    std::optional<std::reference_wrapper<const std::unordered_map<node, node>>> nodeIdMap)
    : G(&G), nodeIdMap(nodeIdMap) {
    if (!G.isDirected())
        throw std::runtime_error("Topological sort is defined for directed graphs only.");
}

void TopologicalSort::run() {
    reset();

    std::stack<node> nodeStack;

    G->forNodes([&](node u) {
        node mappedU;
        if (nodeIdMap.has_value())
            mappedU = nodeIdMap.value().get().at(u);
        else
            mappedU = u;

        if (topSortMark[mappedU] == NodeMark::PERM)
            return;

        nodeStack.push(u);
        do {
            node v = nodeStack.top();
            node mappedV;
            if (nodeIdMap.has_value())
                mappedV = nodeIdMap.value().get().at(v);
            else
                mappedV = v;

            if (topSortMark[mappedV] != NodeMark::NONE) {
                nodeStack.pop();
                if (topSortMark[mappedV] == NodeMark::TEMP) {
                    topSortMark[mappedV] = NodeMark::PERM;
                    topology[current] = v;
                    current--;
                }
            } else {
                topSortMark[mappedV] = NodeMark::TEMP;
                G->forNeighborsOf(v, [&](node w) {
                    node mappedW;
                    if (nodeIdMap.has_value())
                        mappedW = nodeIdMap.value().get().at(w);
                    else
                        mappedW = w;

                    if (topSortMark[mappedW] == NodeMark::NONE)
                        nodeStack.push(w);
                    else if (topSortMark[mappedW] == NodeMark::TEMP)
                        throw std::runtime_error("Error: the input graph has cycles.");
                });
            }
        } while (!nodeStack.empty());
    });

    hasRun = true;
}

void TopologicalSort::reset() {
    // Reset node marks
    count n = G->numberOfNodes();
    if (n == 0)
        throw std::runtime_error("Graph should contain at least one node.");

    if (n != static_cast<count>(topSortMark.size())) {
        topSortMark.resize(n);
        topology.resize(n);
    }
    std::fill(topSortMark.begin(), topSortMark.end(), NodeMark::NONE);
    std::fill(topology.begin(), topology.end(), 0);
    // Reset current
    current = n - 1;
}

} // namespace NetworKit
