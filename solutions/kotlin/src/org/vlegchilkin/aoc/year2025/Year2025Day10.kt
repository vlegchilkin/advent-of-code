package org.vlegchilkin.aoc.year2025

import com.microsoft.z3.*
import org.vlegchilkin.aoc.*


data class Machine(val lights: Int, val buttons: List<Int>, val joltage: List<Int>)

/**
 * 2025/10: Factory
 *
 * don't forget env variable DYLD_LIBRARY_PATH=~/microsoft/z3/build
 *
 * cd ~/microsoft
 * git clone https://github.com/Z3Prover/z3.git
 * cd ~/microsoft/z3
 * python3 scripts/mk_make.py --java
 * cd build
 * make
 */
class Year2025Day10(input: String) : Solution {
  private val machines: List<Machine>

  init {
    val pattern = """^\[([.#]+)] (.*) \{([\d,]+)}$""".toRegex()
    machines = input.toList { line ->
      val (a, b, c) = pattern.matchEntire(line)!!.destructured
      Machine(
        lights = a.reversed().fold(0) { acc, c -> (acc shl 1) or (c == '#').toInt() },
        buttons = b.split(' ').map { group ->
          val lights = group.removeSurrounding("(", ")").split(',').map { it.toInt() }
          lights.fold(0) { acc, c -> acc or (1 shl c) }
        },
        joltage = c.split(',').map { it.toInt() }
      )
    }
  }

  override fun partA(): Any {
    fun solve(machine: Machine): Int {
      for (packSize in 1..machine.buttons.size) {
        machine.buttons.combinations(packSize).forEach { pressed ->
          val state = pressed.fold(0) { acc, button -> acc xor button }
          if (state == machine.lights) return packSize
        }
      }
      error("not possible")
    }

    return machines.sumOf { solve(it) }
  }

  override fun partB(): Any {
    fun solve(machine: Machine): Int {
      val ctx = Context()
      val x = machine.buttons.indices.map { ctx.mkIntConst("x$it") }.toTypedArray()
      val a = machine.buttons.mapIndexed { i, button ->
        machine.joltage.indices.map { if (button and (1 shl it) == 0) 0 else 1 }.toTypedArray()
      }
      val c = machine.joltage.toTypedArray()


      val eqs = c.mapIndexed { j, cj ->
        val exprs = a.mapIndexed { i, row ->
          ctx.mkMul(ctx.mkInt(row[j]), x[i])
        }.toTypedArray()

        ctx.mkEq(ctx.mkAdd(*exprs), ctx.mkInt(c[j]))
      }.toTypedArray()

      val opt = ctx.mkOptimize()

      opt.Add(*eqs)
      x.forEach { opt.Add(ctx.mkGe(it, ctx.mkInt(0))) }

      opt.MkMinimize(ctx.mkAdd(*x))

      require(opt.Check() === Status.SATISFIABLE) { "No integer solution exists." }
      val model = opt.model
      val result = x.map { model.evaluate(it, false).toString().toInt() }
      return result.sum()
    }

    return machines.sumOf { solve(it) }
  }

  companion object : Test(2025, 10, { Year2025Day10(it) })
}
