package org.vlegchilkin.aoc


import org.ejml.data.DMatrixRMaj
import org.ejml.dense.row.factory.LinearSolverFactory_DDRM

fun List<Number>.polyfit(degree: Int): DoubleArray {
  return polyfitDouble(this.mapIndexed { i, value -> i.toDouble() to value.toDouble() }, degree)
}


/**
 *     Least squares polynomial fit.
 *
 *     Fit a polynomial ``p(x) = p[0] * x**degree + ... + p[degree]`` of degree `degree`
 *     to points `(x, y)`. Returns a vector of coefficients `p` that minimises
 *     the squared error in the order `0`, ... , `deg-1`, `deg`
 *
 */
fun polyfitDouble(points: List<Pair<Double, Double>>, degree: Int): DoubleArray {
  val numRows = degree + 1
  val c = DMatrixRMaj(numRows, 1) // matrix containing computed polynomial coefficients
  val o = DMatrixRMaj(points.map { it.second }.toDoubleArray())  // observation matrix

  val a = DMatrixRMaj(o.numRows, numRows)   // Vandermonde matrix
  points.mapIndexed { i, (x, _) ->
    var obs = 1.0
    for (j in 0 until numRows) {
      a.set(i, j, obs)
      obs *= x
    }
  }

  val solver = LinearSolverFactory_DDRM.linear(numRows)
  if (solver.setA(a)) solver.solve(o, c) else error("Solver failed")

  return c.data
}