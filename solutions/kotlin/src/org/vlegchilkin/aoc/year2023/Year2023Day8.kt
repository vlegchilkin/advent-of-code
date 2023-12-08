package org.vlegchilkin.aoc.year2023

import org.vlegchilkin.aoc.*


/**
 * 2023/8: Haunted Wasteland
 */
class Year2023Day8(input: String) : Solution {
  private val instructions: CharArray
  private val graph: Map<String, Pair<String, String>>

  init {
    val (instr, data) = input.toList("\n\n") { it }
    instructions = instr.toCharArray()
    val regex = """^(.{3}) = \((.{3}), (.{3})\)$""".toRegex()
    graph = data.toList { it }.associate { d ->
      val (src, left, right) = regex.matchEntire(d)!!.destructured
      src to (left to right)
    }
  }

  private fun loopSize(start: String): Int {
    var step = 0
    var pos = start
    while (pos.last() != 'Z') {
      pos = graph[pos]!!.let { if (instructions[step % instructions.size] == 'L') it.first else it.second }
      step += 1
    }
    return step
  }

  override fun partA(): Any {
    return loopSize("AAA")
  }

  override fun partB(): Any {
    val sizes = graph.keys.filter { it.last() == 'A' }.map { loopSize(it) }
    return sizes.lcm()
  }

  companion object : Test(2023, 8, { Year2023Day8(it) })
}
