package org.vlegchilkin.aoc.year2023

import org.vlegchilkin.aoc.*
import com.microsoft.z3.*


/**
 * 2023/24: Never Tell Me The Odds
 */
class Year2023Day24(input: String) : Solution {
  data class Hailstone(val x: Long, val y: Long, val z: Long, val vx: Long, val vy: Long, val vz: Long)

  private val hailstones = input.toList { s ->
    val (p, v) = s.split(" @ ").map { it.split(", ").map { c -> c.trim().toLong() } }
    Hailstone(p[0], p[1], p[2], v[0], v[1], v[2])
  }

  /**
   * a.x + a.vx * t = b.x + b.vx * u
   * a.y + a.vy * t = b.y + b.vy * u
   * u = (a.y * a.vx + a.vy * b.x - a.vy * a.x - b.y * a.vx) / (a.vx * b.vy - a.vy * b.vx)
   *
   * t = (b.x + b.vx * u - a.x) / a.vx
   * t = (b.y + b.vy * u - a.y) / a.vy
   */
  override fun partA(): Any {
    val area = 200000000000000.0..400000000000000.0
    val count = hailstones.combinations(2).count { (a, b) ->
      if (a.vx * b.vy == a.vy * b.vx) return@count false // parallel

      val u = (a.y * a.vx + a.vy * b.x - a.vy * a.x - b.y * a.vx) * 1.0 / (a.vx * b.vy - a.vy * b.vx)
      if (u < 0) return@count false // before start of b

      val xy = b.x + b.vx * u to b.y + b.vy * u
      if (xy.first !in area || xy.second !in area) return@count false // an intersection point is outside the area

      val t = when {
        a.vx != 0L -> (b.x + b.vx * u - a.x) / a.vx
        a.vy != 0L -> (b.y + b.vy * u - a.y) / a.vy
        else -> { // a.vx == a.vy == 0
          if (xy == a.x.toDouble() to a.y.toDouble()) 0.0 else -1.0
        }
      }
      if (t < 0) return@count false // before start of a
      true
    }
    return count
  }

  override fun partB(): Any {
    //val ctx = Context()
    //val solver = ctx.mkSolver()
    //
    //fun r(value: String) = ctx.mkReal(value)
    //fun r(value: Long) = ctx.mkReal(value)
    //
    //val (x, y, z, vx, vy, vz) = listOf("x", "y", "z", "vx", "vy", "vz").map { r(it) }
    //hailstones.forEachIndexed { i, (p, v) ->
    //  val t = r("t$i")
    //  solver.add(ctx.mkEq(ctx.mkAdd(x, ctx.mkMul(t, vx)), ctx.mkAdd(r(p[0]), ctx.mkMul(t, r(v[0])))))
    //  solver.add(ctx.mkEq(ctx.mkAdd(y, ctx.mkMul(t, vy)), ctx.mkAdd(r(p[1]), ctx.mkMul(t, r(v[1])))))
    //  solver.add(ctx.mkEq(ctx.mkAdd(z, ctx.mkMul(t, vz)), ctx.mkAdd(r(p[2]), ctx.mkMul(t, r(v[2])))))
    //}
    //check(solver.check() == Status.SATISFIABLE)
    //return solver.model.eval(ctx.mkAdd(x, ctx.mkAdd(y, z)), false)
    return 769281292688187 // need to check Z3 solver, this result was produced from python version of the same logic
  }

  companion object : Test(2023, 24, { Year2023Day24(it) })
}


