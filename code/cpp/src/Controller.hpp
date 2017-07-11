#ifndef CONTROLLER_HPP
#define CONTROLLER_HPP

#include <memory>
#include <string>
#include "ProblemInstance.hpp"

class Solver;

class Controller {
public:
    Controller();
    ~Controller();
    void generateInstance(int numTasks, int numSubsets, int numSubsetsToSelect);
    const std::string& getInstanceName() const { return _instanceName; }
    const ProblemInstance * getProblemInstance() const {
        return _problemInstance.get();
    }
    void initSolverWithProblemData();
    Solver * getSolver() { return _solver.get(); }

private:
    typedef std::unique_ptr<ProblemInstance> ProbUPtr;
    ProbUPtr _problemInstance;
    std::string _instanceName;
    std::unique_ptr<Solver> _solver;
};

#endif
