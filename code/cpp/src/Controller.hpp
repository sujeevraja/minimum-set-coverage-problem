#ifndef CONTROLLER_HPP
#define CONTROLLER_HPP

#include <memory>
#include <string>

class ProblemInstance;
class Solver;

class Controller {
public:
    Controller();
    ~Controller();
    void generateInstance(int numTasks, int numSubsets, int numSubsetsToSelect);
    const std::string& getInstanceName() const { return _instanceName; }
    void writeProblemData() const;
    const ProblemInstance * getProblemInstance() const;
    Solver * getSolver();
    void addProblemDataToSolver();

private:
    typedef std::unique_ptr<ProblemInstance> ProbUPtr;
    ProbUPtr _problemInstance;
    std::unique_ptr<Solver> _solver;
    std::string _instanceName;
};

#endif
