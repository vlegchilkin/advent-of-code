package org.vlegchilkin.aoc.year2025

import org.vlegchilkin.aoc.*
import java.util.function.LongBinaryOperator


/**
 * 2025/6: Trash Compactor
 */
class Year2025Day6(input: String) : Solution {
  private val lines = input.toList { it }

  override fun partA(): Any {
    val parsed = lines.map { it.trim().split("\\s+".toRegex()) }
    val n = parsed[0].size

    fun solve(k: Int): Long {
      val op = if (parsed.last()[k] == "+") LongBinaryOperator { a, b -> a + b } else LongBinaryOperator { a, b -> a * b }
      return parsed.dropLast(1).map { it[k].toLong() }.reduce { a, b -> op.applyAsLong(a, b) }
    }

    return (0 until n).sumOf { i -> solve(i) }
  }

  override fun partB(): Any {
    val operators = lines.last()
    val numbers = lines.dropLast(1)
    val offsets = operators.trim().split("[+*]".toRegex())
      .mapNotNull { col -> col.length.takeIf { it > 0 }?.let { it + 1 } }
      .runningFold(0) { acc, col -> acc + col }

    val n = offsets.size
    val borderOffset = lines.maxOf { it.length } + 1

    fun solve(k: Int): Long {
      val start = offsets[k]
      val end = (if (k == n - 1) borderOffset else offsets[k + 1])

      var result: Long
      val op = if (operators[start] == '+') {
        result = 0L
        LongBinaryOperator { a, b -> a + b }
      }
      else {
        result = 1L
        LongBinaryOperator { a, b -> a * b }
      }

      for (idx in start until end - 1) {
        val num = numbers
          .mapNotNull { line -> line[idx].takeIf { it.isDigit() }?.let { it - '0' } }
          .fold(0L) { acc, num -> acc * 10 + num }
        result = op.applyAsLong(result, num)
      }

      return result
    }

    return (0 until n).sumOf { i -> solve(i) }
  }

  companion object : Test(2025, 6, { Year2025Day6(it) })
}
