package org.vlegchilkin.aoc.year2024

import org.vlegchilkin.aoc.*
import org.vlegchilkin.aoc.year2024.ChronoSpatialComputer.OpCode.*


class ChronoSpatialComputer(private val program: List<Int>) {
  enum class OpCode(val value: Int) {
    ADV(0), BXL(1), BST(2), JNZ(3), BXC(4), OUT(5), BDV(6), CDV(7);

    companion object {
      fun of(value: Int) = entries.find { it.value == value } ?: error("Unknown opcode $value")
    }
  }

  fun run(registerInitValues: List<Long>): List<Int> {
    val registers = registerInitValues.toLongArray()
    val output: MutableList<Int> = mutableListOf()
    var pointer = 0

    fun nextLiteral(): Int = program[pointer++]
    fun nextComboOperand(): Long = when (val operand = nextLiteral()) {
      in 0..3 -> operand.toLong()
      in 4..6 -> registers[operand - 4]
      else -> error("Non-supported combo operand $operand")
    }

    while (pointer <= program.lastIndex) {
      when (OpCode.of(nextLiteral())) {
        ADV -> {
          registers[0] = registers[0] shr nextComboOperand().toInt()
        }
        BXL -> {
          registers[1] = registers[1] xor nextLiteral().toLong()
        }
        BST -> {
          registers[1] = nextComboOperand() % 8
        }
        JNZ -> {
          val reference = nextLiteral()
          if (registers[0] != 0L) pointer = reference
        }
        BXC -> {
          nextLiteral()
          registers[1] = registers[1] xor registers[2]
        }
        OUT -> {
          output.add(nextComboOperand().mod(8))
        }
        BDV -> {
          registers[1] = registers[0] shr nextComboOperand().toInt()
        }
        CDV -> {
          registers[2] = registers[0] shr nextComboOperand().toInt()
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
  private val registerInitValues: List<Long>
  private val program: List<Int>

  init {
    val (registers, program) = input.toList("\n\n") { it.toIntList() }
    this.registerInitValues = registers.map { it.toLong() }
    this.program = program
  }

  override fun partA(): String {
    val output = ChronoSpatialComputer(program).run(registerInitValues)
    return output.joinToString(separator = ",")
  }

  override fun partB(): Long {
    val computer = ChronoSpatialComputer(program)

    fun dfs(prefix: Long, len: Int): Long? {
      if (len == program.size) return prefix
      val expected = program.takeLast(len + 1)
      val possibleA = IntRange(0, 7).map { (prefix shl 3) + it }
      val solution = possibleA.firstNotNullOfOrNull { regA ->
        val output = computer.run(listOf(regA, 0, 0))
        if (output == expected) dfs(regA, len + 1) else null
      }
      return solution
    }

    val minA = dfs(0L, 0) ?: error("Part b has no solution")
    return minA
  }

  companion object : Test(2024, 17, { Year2024Day17(it) })
}
