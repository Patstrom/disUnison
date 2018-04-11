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
            cerr << "Addin strategy \"difference\"" << endl;
            continue;
        }
        if(s == "schedule") {
            functions.push_back(schedule);
            cerr << "Addin strategy \"schedule\"" << endl;
        }
        if(s == "registers") {
            functions.push_back(registers);
            cerr << "Addin strategy \"registers\"" << endl;
        }
    }

   return functions;
}

void Diversity::registers(GlobalModel& home, const GlobalModel& b) {
    BoolVarArgs equal_old(home, home.v_r.size(), 0, 1);
    for(int i = 0; i < home.v_r.size(); i++) {
        rel(home, home.v_r[i], IRT_EQ, b.v_r[i].val(), equal_old[i]); // equal_old[i] is true if v_r[i] equal b.v_r[i]
    }

    rel(home, BOT_AND, equal_old, 0); // ^ across equal_old equal 0 (i.e not all equal_old[i] is true)
}


void Diversity::schedule(GlobalModel& home, const GlobalModel& b) {
// WIP
//
//    BoolVarArgs equal_old(*this, v_c.size(), 0, 1);
//    for(int i = 0; i < v_c.size(); i++) {
//        rel(*this, v_c[i], IRT_EQ, b.v_c[i].val(), equal_old[i]);
//    }
//
//    rel(*this, BOT_AND, equal_old, 0);
}
