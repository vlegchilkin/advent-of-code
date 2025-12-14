package org.vlegchilkin.aoc.year2025

import org.vlegchilkin.aoc.*


/**
 * 2025/6: Trash Compactor
 */
class Year2025Day6(input: String) : Solution {
  private val lines = input.toList { it }

  override fun partA(): Any {
    val parsed = lines.map { it.trim().split("\\s+".toRegex()) }
    val n = parsed[0].size

    fun solve(k: Int): Long {
      val numbers = parsed.dropLast(1).map { it[k].toLong() }
      return when (parsed.last()[k]) {
        "+" -> numbers.reduce { a, b -> a + b }
        else -> numbers.reduce { a, b -> a * b }
      }
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

      val numbers = (start until end - 1).map { idx ->
        val digits = numbers.mapNotNull { line -> line[idx].takeIf { it.isDigit() }?.let { it - '0' } }
        digits.fold(0L) { acc, num -> acc * 10 + num }
      }

      return when (operators[start]) {
        '+' -> numbers.reduce { acc, col -> acc + col }
        else -> numbers.reduce { acc, col -> acc * col }
      }
    }

    return (0 until n).sumOf { i -> solve(i) }
  }

  companion object : Test(2025, 6, { Year2025Day6(it) })
}
