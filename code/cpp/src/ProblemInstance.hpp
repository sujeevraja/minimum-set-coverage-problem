#ifndef PROBLEM_INSTANCE_HPP
#define PROBLEM_INSTANCE_HPP

#include <vector>
#include <string>

class ProblemInstance {
public:
    ProblemInstance(const int numTasks, const int numSubsets, const int numSubsetsToSelect);
    int getNumTasks() const { return _numTasks; }
    int getNumSubsets() const { return _numSubsets; }
    int getNumSubsetsToSelect() const { return _numSubsetsToSelect; }
    void print() const;
    void writeToFile(const std::string& fileName) const;
    const std::vector<std::vector<int>>& getSubsets() const { return _subsets; }
    std::string getName() const;

private:
    int _numTasks;
    int _numSubsets;
    int _numSubsetsToSelect;
    std::vector<std::vector<int>> _subsets;
    std::string _timeStampStr;
};

#endif
