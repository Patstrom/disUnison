/*
 *  Main authors:
 *    Patrik Karlström <pkarlstr@kth.se>
 *
 *  This file is part of Unison, see http://unison-code.github.io
 *
 *  Copyright (c) 2016, RISE SICS AB
 *  All rights reserved.
 *
 *  Redistribution and use in source and binary forms, with or without
 *  modification, are permitted provided that the following conditions are met:
 *  1. Redistributions of source code must retain the above copyright notice,
 *     this list of conditions and the following disclaimer.
 *  2. Redistributions in binary form must reproduce the above copyright notice,
 *     this list of conditions and the following disclaimer in the documentation
 *     and/or other materials provided with the distribution.
 *  3. Neither the name of the copyright holder nor the names of its
 *     contributors may be used to endorse or promote products derived from this
 *     software without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 *  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 *  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 *  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
 *  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 *  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 *  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 *  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 *  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 *  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 *  POSSIBILITY OF SUCH DAMAGE.
 */

#include "diversitymodel.hpp"

DiversityModel::DiversityModel(GlobalModel* gm) : GlobalModel(*gm) {}

DiversityModel::DiversityModel(DiversityModel& cg) :
  GlobalModel(cg) {}

DiversityModel* DiversityModel::copy(void) {
  return new DiversityModel(*this);
}

void DiversityModel::constrain(const Space& _b) {
    const GlobalModel& b = static_cast<const GlobalModel&>(_b);

    string diversity_strategy = options->diversify();
    if (diversity_strategy == "registers") {
        // ~(x_p ^ ry_p)
        // in words: make sure that the next solution does not have the same connected operands and the same operands to register allocation
        BoolVarArgs lits;
        for (operand p: input->P) {
	  lits << var(x(p) == b.x(p).val());
          lits << var(ry(p) == b.ry(p).val());
        }
        if (lits.size() > 0) rel(*this, BOT_AND, lits, 0);

    } else if (diversity_strategy == "difference") {
        // Do nothing
    } else if (diversity_strategy == "schedule") {
	// ~(a_o ^ c_o ^ i_o)
	// in words: make sure that the next solution does not have the exact same active operations, issue cycles and instructions as the previous one
	BoolVarArgs lits;
	for (operation o: input->O) {
	  lits << var(a(o) == b.a(o).val());
	  if(b.a(o).val()) {
	    lits << var(c(o) == b.c(o).val());
	    lits << var(i(o) == b.i(o).val());
          }
	}
	if (lits.size() > 0) rel(*this, BOT_AND, lits, 0);
    }
}
