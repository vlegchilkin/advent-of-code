package org.vlegchilkin.aoc.year2024

import org.vlegchilkin.aoc.*

class Computer(program: List<String>) {
  companion object {
    val INSTRUCTION_REGEX = """mul\(-?\d+,-?\d+\)|do\(\)|don't\(\)""".toRegex()
  }

  private val instructions = program.map { line ->
    INSTRUCTION_REGEX.findAll(line).map { mul -> mul.groupValues[0] }.toList()
  }.flatten()

  fun run(filter: (String) -> Boolean = { _ -> true }): Int {
    var isActive = true
    var result = 0

    instructions.filter(filter).forEach { instr ->
      if (instr == "do()") isActive = true
      else if (instr == "don't()") isActive = false
      else if (!isActive) return@forEach

      result += when {
        instr.startsWith("mul(") -> instr.toIntList().reduce { a, b -> a * b }
        else -> error("$instr is not supported")
      }
    }

    return result
  }
}

/**
 * 2024/3: Mull It Over
 */
class Year2024Day3(input: String) : Solution {
  private val lines = input.toList { it }

  override fun partA(): Int {
    return Computer(lines).run { it.startsWith("mul") }
  }

  override fun partB(): Any {
    return Computer(lines).run()
  }

  companion object : Test(2024, 3, { Year2024Day3(it) })
}
