#include <boost/optional.hpp>
#include <numeric>
#include <iostream>
#include <sstream>
#include "Controller.hpp"
#include "Solver.hpp"
#include "Utility.hpp"

void Controller::generateInstance(int numTasks, int numSubsets, int numSubsetsToSelect) {
    _problemInstance = ProbUPtr(new ProblemInstance(numTasks, numSubsets, numSubsetsToSelect));
    _instanceName = _problemInstance->getName();

    _problemInstance->print();
    const std::string folderName = "data";
    if (util::folderExists(folderName))
    {
       const std::string instanceFileName = "data/" + _instanceName + ".txt";
       _problemInstance->writeToFile(instanceFileName);
    }
    else
    {
       std::cout << "WARN: could not find folder " << folderName << "."
          << " problem data not written.\n";
    }
}

void Controller::solveInstance() {
    Solver solver;

    // add task variables.
    const int numTasks = _problemInstance->getNumTasks();
    for(int i = 0; i < numTasks; ++i) {
        std::stringstream oss;
        oss << "task_" << i;
        const std::string colName = oss.str();
        solver.addColumn(i, 0.0, 1.0, 1.0, &colName);
    }

    // add subset variables.
    const int numSubsets = _problemInstance->getNumSubsets();
    for(int i = 0; i < numSubsets; ++i) {
        std::stringstream oss;
        oss << "subset_" << i;
        const std::string colName = oss.str();
        solver.addColumn(numTasks + i, 0.0, 1.0, 0.0, &colName);
    }

    // mark all variables as integer.
    const int numCols = numTasks + numSubsets;
    for(int i = 0; i < numCols; ++i)
        solver.markColAsInteger(i);

    // add VUB constraints.
    std::vector<double> rowCoefs({1.0, -1.0});
    std::vector<int> rowIndices(2, 0);
    {
        const std::vector<std::vector<int>>& subsets = _problemInstance->getSubsets();
        for(int i = 0; i < static_cast<int>(subsets.size()); ++i) {
            const auto& subset = subsets[i];
            for(const int taskIndex : subset) {
                rowIndices[0] = numTasks + i;
                rowIndices[1] = taskIndex;
                solver.addRow(rowIndices, rowCoefs, boost::none, 0.0);
            }
        }
    }

    // add cardinality constraint.
    const int numSubsetsToSelect = _problemInstance->getNumSubsetsToSelect();
    rowCoefs = std::vector<double>(numSubsets, 1.0);
    rowCoefs.resize(numSubsets, 1.0);
    rowIndices.resize(numSubsets);
    std::iota(rowIndices.begin(), rowIndices.end(), numTasks);
    solver.addRow(rowIndices, rowCoefs, numSubsetsToSelect, boost::none);

    // solve model
    // solver.printModelData();
    solver.solveWithCbc();
}
