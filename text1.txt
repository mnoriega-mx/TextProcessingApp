// g++ -std=c++11 kwp.cpp -o kwp   
// ./kwp <matrix_file.txt>

#include <iostream>
#include <vector>
#include <unordered_map>
#include <string>
#include <algorithm>
#include <list>
#include <fstream>
#include <sstream>

using namespace std;

struct Edge {
    int src;
    int dest;
    int weight;
};

// Function to check if a node is already included in the MST
bool Find(int num, vector<Edge>& mst) {
    for (int i = 0; i < mst.size(); i++) {
        if ((mst[i].src == num) || (mst[i].dest == num)) {
            // found num (node) in set
            return true;
        }
    }
    // did not find num (node) in set
    return false;
}

bool FindColor(int num, vector<int>& colors) {
    for (int i = 0; i < colors.size(); i++) {
        if (colors[i] == num) {
            return true;
        }
    }
    return false;
}

int FindMissingHalf(int num, list<pair<int,int>>& numAristas) {
    list<pair<int,int>> copy = numAristas;
    while (!copy.empty()) {
        if (copy.front().first == num) {
            return copy.front().second;
        }
        copy.pop_front();
    }
    return -1;
}

void PrintMatrix(const vector<vector<int>>& matrix) {
    for (int i = 0; i < matrix.size(); i++) {
        for (int j = 0; j < matrix[i].size(); j++) {
            cout << matrix[i][j] << " ";
        }
        cout << endl;
    }
}

// Function implementing Kruskal's algorithm to return the MST adjacency matrix
vector<vector<int>> kruskalMST(const vector<vector<int>>& graph) {
    vector<Edge> edges;

    // solo tomamos el triangulo superior de la matriz (ya que es simetrica)
    for (int i = 0; i < graph.size(); i++) {
        for (int j = i; j < graph[i].size(); j++) {
            if (graph[i][j] != 0) {
                edges.push_back({i, j, graph[i][j]});
            }
        }
    }

    // ordenamos las aristas por peso
    sort(edges.begin(), edges.end(), [](Edge a, Edge b) {
        return a.weight < b.weight;
    });

    // obtenemos mst
    vector<Edge> mst;
    for (int i = 0; i < edges.size(); i++) {
        if ((!Find(edges[i].src, mst)) || (!Find(edges[i].dest, mst))) {
            mst.push_back(edges[i]);
        }
    }

    cout << endl << "Aristas del árbol de expansión mínima (MST):" << endl;
    cout << "src \tdest \tweight" << endl;
    int totalWeight = 0;
    for (int i = 0; i < mst.size(); i++) {
        cout << mst[i].src << " \t" << mst[i].dest << " \t" << mst[i].weight << endl;
        totalWeight += mst[i].weight;
    }

    cout << endl << "Peso total del árbol de expansión mínima (MST): " << totalWeight << endl;

    // crear matriz de adyacencia del mst en el estilo de input
    vector<vector<int>> mst_graph(graph.size(), vector<int>(graph.size(), 0));
    for (int i = 0; i < mst.size(); i++) {
        mst_graph[mst[i].src][mst[i].dest] = mst[i].weight;
        mst_graph[mst[i].dest][mst[i].src] = mst[i].weight;
    }

    cout << endl << "Matriz de adyacencia del árbol de expansión mínima (MST):" << endl;
    // imprimir la matriz de adyacencia del MST
    PrintMatrix(mst_graph);

    return mst_graph;
}

// Welsh-Powell function
void welshPowell(const vector<vector<int>>& graph) {
    vector<vector<int>> maskgraph(graph.size(), vector<int>(graph.size(), 0));
    for (int i = 0; i < graph.size(); i++) {
        for (int j = 0; j < graph[i].size(); j++) {
            if (graph[i][j] != 0) {
                maskgraph[i][j] = -1;
            }
        }
    }

    vector<int> colors;
    list<pair<int,int>> numAristas;
    int count = 0;
    for (int i = 0; i < graph.size(); i++) {
        count = 0;
        for (int j = 0; j < graph.size(); j++) {
            if (maskgraph[i][j] != 0) {
                count++;
            }
        }
        numAristas.push_back(pair<int,int>(i, count));
    }

    numAristas.sort([](pair<int,int> a, pair<int,int> b) {
        return a.second > b.second;
    });

    list<pair<int,int>> numAristasCopy = numAristas;

    cout << endl << "Welsh-Powell max heap: " << endl;
    cout << "Vértice \tAristas" << endl;
    while(!numAristasCopy.empty()){
        cout << numAristasCopy.front().first << "\t\t" << numAristasCopy.front().second << endl;
        numAristasCopy.pop_front();
    }
    /*
    cout << endl << "Maskgraph:" << endl;
    PrintMatrix(maskgraph);
    */

    int color = 1;
    while (!numAristas.empty()) {
        // find node with most edges
        int node = numAristas.front().first;
        numAristas.pop_front();

        // assign color to node
        maskgraph[node][node] = color;

        // if color is not in colors, add it
        if (!FindColor(color, colors)) {
            colors.push_back(color);
        }

        for (int j = 0; j < maskgraph[node].size(); j++) {
            if (maskgraph[node][j] != -1 && maskgraph[j][j] == 0) {
                maskgraph[j][j] = color;

                int half = FindMissingHalf(j, numAristas);
                numAristas.remove(pair<int,int>(j, half));
            }
        }
        color++;
    }

    cout << endl << "Colores usados: ";
    for (int i = 0; i < colors.size(); i++) {
        cout << colors[i] << " ";
    }

    cout << endl << "Vértice \tColor" << endl;
    for (int i = 0; i < maskgraph.size(); i++) {
        cout << i << "\t\t" << maskgraph[i][i] << endl;
    }
}

// Function to read the matrix from the file
vector<vector<int>> readMatrixFromFile(const string& filename) {
    ifstream file(filename);
    vector<vector<int>> matrix;
    string line;

    while (getline(file, line)) {
        vector<int> row;
        istringstream iss(line);
        int num;
        while (iss >> num) {
            row.push_back(num);
        }
        matrix.push_back(row);
    }

    return matrix;
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        cout << "Usage: " << argv[0] << " <matrix_file.txt>" << endl;
        return 1;
    }

    // Read the matrix from the provided file
    string filename = argv[1];
    vector<vector<int>> graph = readMatrixFromFile(filename);

    // imprimir la matriz de adyacencia del grafo original
    cout << "Matriz de adyacencia del grafo original:" << endl;
    PrintMatrix(graph);

    // llamamos la función kruskalMST para obtener la matriz de adyacencia del MST
    kruskalMST(graph);

    // llamar a la función Welsh-Powell
    welshPowell(graph);

    return 0;
}
