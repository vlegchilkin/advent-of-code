package org.vlegchilkin.aoc.year2024

import org.vlegchilkin.aoc.*

data class Equation(val total: Long, val elements: List<Long>) {
  fun isPossible(allowedOperators: String): Boolean {

    fun dfs(idx: Int = 0, sum: Long = 0): Boolean {
      if (idx == elements.size) return sum == total
      if (sum > total) return false
      if (idx == 0) return dfs(1, elements[0])

      for (operator in allowedOperators) {
        val nSum = when (operator) {
          '+' -> sum + elements[idx]
          '*' -> sum * elements[idx]
          '|' -> "$sum${elements[idx]}".toLong()
          else -> error("Invalid operator: $operator")
        }
        if (dfs(idx + 1, nSum)) return true
      }
      return false
    }

    return dfs()
  }
}

/**
 * 2024/7: Bridge Repair
 */
class Year2024Day7(input: String) : Solution {
  private val equations = input.toList { line ->
    val values = line.toLongList()
    Equation(values.first(), values.drop(1))
  }

  override fun partA(): Any {
    return equations.filter { it.isPossible("+*") }.sumOf { it.total }
  }

  override fun partB(): Any {
    return equations.filter { it.isPossible("+*|") }.sumOf { it.total }
  }

  companion object : Test(2024, 7, { Year2024Day7(it) })
}
