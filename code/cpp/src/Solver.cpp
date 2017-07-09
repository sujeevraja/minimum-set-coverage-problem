#include <iostream>
#include <boost/optional/optional_io.hpp>
#ifdef USE_CBC
#include "CbcModel.hpp"
#include "CoinModel.hpp"
#include "OsiClpSolverInterface.hpp"
#endif
#include "Solver.hpp"
#include "Utility.hpp"

void Solver::addColumn(const int index, const boost::optional<double> lb,
    const boost::optional<double> ub, const double obj, const std::string * name /* = nullptr */) {
    _columns.emplace_back(index, lb, ub, obj, name);
    ++_numCols;
}

void Solver::markColAsInteger(const int index) {
    _integerColIndices.push_back(index);
}

void Solver::addRow(const std::vector<int>& indices, const std::vector<double>& coefs,
    const boost::optional<double> lb, const boost::optional<double> ub) {
    _rowIndices.emplace_back(indices);
    _rowCoefs.emplace_back(coefs);
    _rowBounds.emplace_back(lb, ub);
}

void Solver::solveWithCbc() {
#ifdef USE_CBC
    CoinModel build;

    // add columns
    for(const auto& col : _columns) {
        const double lb = col.lb != boost::none ? col.lb.get() : -COIN_DBL_MAX;
        const double ub = col.ub != boost::none ? col.ub.get() : COIN_DBL_MAX;
        build.setColumnBounds(col.index, lb, ub);
        build.setObjective(col.index, col.obj);
        if(col.name != "")
            build.setColumnName(col.index, col.name.c_str());
    }

    // mark columns as integer
    for(const int index : _integerColIndices)
        build.setInteger(index);

    // add rows to build
    const size_t numRows = _rowIndices.size();
    for(size_t i = 0; i < _rowIndices.size(); ++i) {
        const int numNonZeroes = int(_rowIndices[i].size());
        const double lb = _rowBounds[i].first != boost::none
            ? _rowBounds[i].first.get()
            : -COIN_DBL_MAX;
        const double ub = _rowBounds[i].second != boost::none
            ? _rowBounds[i].second.get()
            : COIN_DBL_MAX;
        build.addRow( numNonZeroes, _rowIndices[i].data(), _rowCoefs[i].data(), lb, ub);
    }

    // // create solver and load data into solver
    OsiSolverInterface * solver = new OsiClpSolverInterface();
    solver->loadFromCoinModel(build);
    build.writeMps("model.mps");

    CbcModel model(*solver);
    model.setLogLevel(0);
    model.setMaximumSeconds(120.0);
    // model.setMaximumNodes(5000);

    // solve model and print solution
    model.branchAndBound();

    std::cout << "solved model.\n";
    std::cout << "number of rows: " << numRows << "\n";
    std::cout << "number of columns: " << model.getNumCols() << "\n";
    std::cout << "status: ";
    if(model.isProvenOptimal())
        std::cout << "optimal\n";
    else if(model.isProvenInfeasible())
        std::cout << "infeasible\n";
    else if(model.isNodeLimitReached())
        std::cout << "reached node limit\n";
    else if(model.isSecondsLimitReached())
        std::cout << "reached time limit\n";
    else
        std::cout << "unknown\n";
    std::cout << "number of nodes: " << model.getNodeCount() << "\n";
    std::cout << "number of iterations: " << model.getIterationCount() << "\n";
    std::cout << "objective value: " << model.getMinimizationObjValue() << "\n";

    const double * const sln = model.solver()->getColSolution();
    for(int i = 0; i < _numCols; ++i)
        _solution.push_back(sln[i]);

    // for duals: use getRowPrice().
    // for a constraint like ax >= b, use getRowActivity() to get ax.

    delete solver;
#else
    const std::string msg = "Cbc include paths and libs not provided Cannot use solveWithCbc().";
    throw util::MSCPException(msg);
#endif
}

void Solver::printModelData() const {
    std::cout << "rows\n";
    for (size_t i = 0; i < _rowIndices.size(); ++i) {
       std::cout << "row " << i << "\n";
       for (size_t j = 0; j < _rowIndices[i].size(); ++j)
          std::cout << " ind " << _rowIndices[i][j] << " coef " << _rowCoefs[i][j] << "\n";
       std::cout << " row lb " << _rowBounds[i].first << " row ub " << _rowBounds[i].second << "\n";
    }
    std::cout << "rows printed\n";
}
