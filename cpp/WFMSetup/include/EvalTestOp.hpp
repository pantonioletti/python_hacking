/* 
 * File:   EvalTestOp.hpp
 * Author: pantonio
 *
 * Created on May 24, 2011, 12:06 PM
 */

#include <beagle/GP.hpp>
#ifndef EVALTESTOP_HPP
#define	EVALTESTOP_HPP
using namespace Beagle;
namespace gpsp{
    class EvalTestOp : GP::EvaluationOp{
public:

  //! SymbRegEvalOp allocator type.
  typedef Beagle::AllocatorT<EvalTestOp,Beagle::GP::EvaluationOp::Alloc>
          Alloc;
  //!< SymbRegEvalOp handle type.
  typedef Beagle::PointerT<EvalTestOp,Beagle::GP::EvaluationOp::Handle>
          Handle;
  //!< SymbRegEvalOp bag type.
  typedef Beagle::ContainerT<EvalTestOp,Beagle::GP::EvaluationOp::Bag>
          Bag;

  explicit EvalTestOp();

  virtual Beagle::Fitness::Handle evaluate(Beagle::GP::Individual& inIndividual,
                                           Beagle::GP::Context& ioContext);
  virtual void postInit(Beagle::System& ioSystem);

protected:

  std::vector<Beagle::Int> mX;
  std::vector<Beagle::Int> mY;
  std::vector<Beagle::Int> mZ;
        
    };
}

#endif	/* EVALTESTOP_HPP */

