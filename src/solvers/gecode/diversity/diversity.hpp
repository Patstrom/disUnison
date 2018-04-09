#ifndef __DIVERSITY__
#define __DIVERSITY

#include "models/globalmodel.hpp"
#include <vector>
#include <functional>
#include <string>
#include <sstream>

typedef std::function<void(GlobalModel*, GlobalModel*)> diversity_function;

namespace Diversity {
    // General functions
    std::vector<std::string> split_comma_seperated(std::string s);
    std::vector<diversity_function> strategies(std::string csl);
    
    // The functions that implements the strategies (posts constraints)
    void registers(GlobalModel* m, GlobalModel* oldm);
    void schedule(GlobalModel* m, GlobalModel* oldm);
}

#endif
