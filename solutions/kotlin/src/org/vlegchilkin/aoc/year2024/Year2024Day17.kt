package org.vlegchilkin.aoc.year2024

import org.vlegchilkin.aoc.*

enum class OpCode(val value: Int) {
  ADV(0), BXL(1), BST(2), JNZ(3), BXC(4), OUT(5), BDV(6), CDV(7);

  companion object {
    fun of(value: Int): OpCode {
      return entries.find { it.value == value }
             ?: error("Unknown opcode $value")
    }
  }
}

class ChronoSpatialComputer(private val memory: List<Int>) {

  fun run(registers: LongArray): List<Int> {
    val output: MutableList<Int> = mutableListOf()
    var pointer = 0
    fun combo(): Long {
      return when (val value = memory[pointer++]) {
        0, 1, 2, 3 -> value.toLong()
        4, 5, 6 -> registers[value - 4]
        else -> error("Non-supported value $value")
      }
    }
    while (pointer <= memory.lastIndex) {
      val opcode = OpCode.of(memory[pointer++])
      when (opcode) {
        OpCode.ADV -> {
          registers[0] = registers[0] shr combo().toInt()
        }
        OpCode.BXL -> {
          registers[1] = registers[1] xor memory[pointer++].toLong()
        }
        OpCode.BST -> {
          registers[1] = combo() % 8
        }
        OpCode.JNZ -> {
          if (registers[0] != 0L) pointer = memory[pointer] else pointer++
        }
        OpCode.BXC -> {
          pointer += 1
          registers[1] = registers[1] xor registers[2]
        }
        OpCode.OUT -> {
          output.add(combo().mod(8))
        }
        OpCode.BDV -> {
          registers[1] = registers[0] shr combo().toInt()
        }
        OpCode.CDV -> {
          registers[2] = registers[0] shr combo().toInt()
        }
      }
    }
    return output
  }

}

/**
 * 2024/17: Chronospatial Computer
 */
class Year2024Day17(input: String) : Solution {
  private val registers: List<Int>
  private val program: List<Int>

  init {
    val (registers, program) = input.toList("\n\n") { it.toIntList() }
    this.registers = registers
    this.program = program
  }

  override fun partA(): String {
    val computer = ChronoSpatialComputer(program)
    val output = computer.run(registers.map { it.toLong() }.toLongArray())
    return output.joinToString(separator = ",")
  }

  override fun partB(): Long {
    val computer = ChronoSpatialComputer(program)

    fun dfs(prefix: Long, len: Int): Long? {
      if (len == program.size) return prefix
      val expected = program.takeLast(len + 1)
      IntRange(0, 7).map { (prefix shl 3) + it }.forEach { regA ->
        if (computer.run(longArrayOf(regA, 0, 0)) == expected) {
          val solution = dfs(regA, len + 1)
          if (solution != null) return solution
        }
      }
      return null
    }

    val minA = dfs(0L, 0) ?: error("Part b has no solution")
    return minA
  }

  companion object : Test(2024, 17, { Year2024Day17(it) })
}
