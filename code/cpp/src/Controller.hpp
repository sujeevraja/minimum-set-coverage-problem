#ifndef CONTROLLER_HPP
#define CONTROLLER_HPP

#include <memory>
#include <string>
#include "ProblemInstance.hpp"

class Solver;

class Controller {
public:
    void generateInstance(int numTasks, int numSubsets, int numSubsetsToSelect);
    void solveInstance();

private:
    typedef std::unique_ptr<ProblemInstance> ProbUPtr;
    ProbUPtr _problemInstance;
    std::string _instanceName;
};

#endif
