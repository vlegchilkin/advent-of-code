package org.vlegchilkin.aoc.year2024

import org.vlegchilkin.aoc.*

data class Equation(val total: Long, val elements: List<Long>) {
  fun isPossible(vararg operators: (Long, Long) -> Long): Boolean {

    fun dfs(idx: Int = 0, sum: Long = 0): Boolean {
      if (idx == elements.size) return sum == total
      if (sum > total) return false
      if (idx == 0) return dfs(1, elements[0])

      return operators.any { operator ->
        dfs(idx + 1, operator(sum, elements[idx]))
      }
    }

    return dfs()
  }
}

/**
 * 2024/7: Bridge Repair
 */
class Year2024Day7(input: String) : Solution {
  private val equations = input.toList { line ->
    Equation(
      total = line.substringBefore(":").toLong(),
      elements = line.substringAfter(":").toLongList()
    )
  }

  override fun partA(): Any {
    val possible = equations.filter {
      it.isPossible(
        Long::plus,
        Long::times
      )
    }

    return possible.sumOf { it.total }
  }

  override fun partB(): Any {
    val possible = equations.filter {
      it.isPossible(
        Long::plus,
        Long::times,
        { a, b -> "$a$b".toLong() }
      )
    }

    return possible.sumOf { it.total }
  }

  companion object : Test(2024, 7, { Year2024Day7(it) })
}
