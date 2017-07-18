#include "Controller.hpp"
#include "ProblemInstance.hpp"
#include "Solver.hpp"
#include <iostream>

int main() {
    try {
        // const int numTasks = 10;
        // const int numSubsets = 8;
        // const int numSubsetsToSelect = 3;
        const int numTasks = 20;
        const int numSubsets = 50;
        const int numSubsetsToSelect = 20;

        std::cout << "Number of tasks (m): " << numTasks << "\n";
        std::cout << "Number of subsets (n): " << numSubsets << "\n";
        std::cout << "Number of subsets to select (k): " << numSubsetsToSelect << "\n";

        Controller controller;
        controller.generateInstance(numTasks, numSubsets, numSubsetsToSelect);
        // controller.getProblemInstance()->printSubsets();
        controller.writeProblemData();
        controller.addProblemDataToSolver();

        auto solver = controller.getSolver();
        // solver->printConstraints();

#ifdef USE_CBC
        solver->prepareDataForCbc();
        const std::string fileName = "data/" + controller.getInstanceName() + ".mps";
        solver->writeModel(fileName);
        solver->solveWithCbc();
#endif
    } catch (const std::exception& e) {
        std::cout << "EXCEPTION: " << e.what() << "\n";
    }

    return 0;
}
