package org.vlegchilkin.aoc.year2020

import org.vlegchilkin.aoc.Test
import org.vlegchilkin.aoc.Solution
import org.vlegchilkin.aoc.trimSplitMap

class Year2020Day8(input: String) : Solution {
  private val original = input.trimSplitMap { line ->
    """^(\w+) ([-+]\d+)$""".toRegex().matchEntire(line)!!.groupValues.let { it[1] to it[2].toInt() }
  }

  private fun runUntilCycle(program: List<Pair<String, Int>>): Pair<Int, Int> {
    val visited = mutableSetOf(program.size)
    var acc = 0
    var pos = 0
    while (pos !in visited) {
      visited.add(pos)
      val (cmd, arg) = program[pos]
      when (cmd) {
        "acc" -> {
          acc += arg
          pos += 1
        }
        "jmp" -> {
          pos += arg
        }
        "nop" -> {
          pos += 1
        }
      }
    }
    return pos to acc
  }

  override fun partA(): Int {
    return runUntilCycle(original).second
  }

  override fun partB(): Int {
    val exchange = mapOf("jmp" to "nop", "nop" to "jmp")
    val buffer = original.toMutableList()
    original.forEachIndexed { i, prev ->
      exchange[prev.first]?.let {
        buffer[i] = it to prev.second
        val (pos, acc) = runUntilCycle(buffer)
        if (pos == buffer.size) return acc
        buffer[i] = prev
      }
    }
    throw IllegalArgumentException("There is not answer")
  }

  companion object : Test(2020, 8, { Year2020Day8(it) })
}