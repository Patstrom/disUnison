#include "diversity.hpp"

std::vector<std::string> Diversity::split_comma_seperated(std::string s) {
    std::vector<std::string> results;
    std::stringstream ss(s);

    while(ss.good()) {
       std::string substr;
       std::getline(ss, substr, ',');
       results.push_back(substr);
   }

   return results;
}


std::vector<diversity_function> Diversity::strategies(std::string csl) {
    std::vector<std::string> strategies = split_comma_seperated(csl);
    
    std::vector<diversity_function> functions;

    for(auto s: strategies) {
        // No switch for strings
        if(s == "difference") {
            // Do nothings. The DFS engine will not explore the same combination twice so
            // by simply not doing anything we get all possible combinations
            continue;
        }
        if(s == "schedule") {
            functions.push_back(schedule);
        }
        if(s == "registers") {
            functions.push_back(registers);
        }
    }

   return functions;
}

void Diversity::registers(GlobalModel* m, GlobalModel* oldm) {
    // Get the register permutation in oldm
}


void Diversity::schedule(GlobalModel* m, GlobalModel* oldm) {
//   // Build the list of values that further solutions cannot be.
//   int oldm_v_c[oldm->v_c.size()];
//   for(int i = 0; i < oldm->v_c.size(); ++i) {
//       // if operation is active we should add it to the list
//       if (oldm->v_a[i].val()) {
//           oldm_v_c[i] = oldm->v_c[i].val();
//       }
//   }
}
