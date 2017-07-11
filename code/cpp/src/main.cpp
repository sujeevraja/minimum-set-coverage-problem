#include "Controller.hpp"
#include "Solver.hpp"
#include <iostream>

int main() {
    try {

        const int numTasks = 10;
        const int numSubsets = 8;
        const int numSubsetsToSelect = 3;

        Controller controller;

        controller.generateInstance(numTasks, numSubsets, numSubsetsToSelect);
        controller.getProblemInstance()->print();

        controller.initSolverWithProblemData();
        Solver * const solver = controller.getSolver();
        // solver->printModelData();
        solver->prepareModelForCbc();
        solver->writeMpsFile(controller.getInstanceName());
        solver->solveWithCbc();

    } catch (const std::exception& e) {
        std::cout << "EXCEPTION: " << e.what() << "\n";
    }

    return 0;
}
