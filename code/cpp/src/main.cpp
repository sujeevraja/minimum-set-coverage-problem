#include "Controller.hpp"
#include <iostream>

int main() {
    try {
        const int numTasks = 10;
        const int numSubsets = 8;
        const int numSubsetsToSelect = 3;

        Controller controller;
        controller.generateInstance(numTasks, numSubsets, numSubsetsToSelect);
        controller.solveInstance();
    } catch (const std::exception& e) {
        std::cout << "EXCEPTION: " << e.what() << "\n";
    }

    return 0;
}
