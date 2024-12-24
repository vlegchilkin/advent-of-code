package org.vlegchilkin.aoc.year2024

import org.vlegchilkin.aoc.*

enum class Command(val op: (Int, Int) -> Int) {
  AND(Int::and),
  XOR(Int::xor),
  OR(Int::or)
}

data class Instruction(val cmd: Command, val in1: String, val in2: String, val out: String)

/**
 * 2024/24: Crossed Wires
 */
class Year2024Day24(input: String) : Solution {
  private val initStates: Map<String, Int>
  private val instructions: List<Instruction>

  init {
    val (initStates, instructions) = input.toList("\n\n") { block -> block.toList { it } }
    this.initStates = initStates.associate { it.substringBefore(':') to it.substringAfter(' ').toInt() }
    this.instructions = instructions.map { line ->
      val (in1, cmd, in2, _, out) = line.split(' ')
      Instruction(Command.valueOf(cmd), in1, in2, out)
    }
  }

  override fun partA(): Long {
    val outputs = instructions.associateBy { it.out }
    val states = initStates.toMutableMap()
    fun dfs(pin: String): Int {
      states[pin]?.let { return it }
      val instruction = outputs[pin] ?: error("No output for $pin")
      val out = with(instruction) {
        val a = dfs(in1)
        val b = dfs(in2)
        cmd.op(a, b)
      }
      return out.also { states[pin] = it }
    }

    val zPins = outputs.keys.filter { it.startsWith('z') }.sortedDescending()
    val result = zPins.fold(0L) { res, pin ->
      (res shl 1) + dfs(pin)
    }
    return result
  }

  /**
   *  solved manually via graph picture rendered on python
   *  @see [solutions/python/aoc/year_2024/day_24_graph.png]
   */
  override fun partB(): Any {
    val result = listOf("z14", "vss", "hjf", "kdh", "z31", "kpp", "z35", "sgj").sorted()
    return result.joinToString(",")
  }

  companion object : Test(2024, 24, { Year2024Day24(it) })
}
