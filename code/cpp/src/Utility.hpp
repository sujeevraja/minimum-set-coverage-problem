#ifndef UTILITY_HPP
#define UTILITY_HPP

#include <algorithm>
#include <stdexcept>
#include <string>

namespace util {
    struct MSCPException : public std::runtime_error {
        MSCPException(const std::string& message)
            : std::runtime_error(message) {}
    };

    std::string getCurrentTimeStamp();

    bool folderExists(const std::string& dirName);
}

#endif
