package org.vlegchilkin.aoc.year2025

import org.vlegchilkin.aoc.*


/**
 * 2025/3: Lobby
 */
class Year2025Day3(input: String) : Solution {
  private val banks = input.toList { it }

  private fun solve(n: Int): Long {
    val values = banks.map { bank ->
      var value = 0L
      var startPos = 0
      for (p in 1..n) {
        val maxNum = bank.drop(startPos).dropLast(n - p).max()
        startPos = bank.indexOf(maxNum, startPos) + 1
        value = value * 10 + (maxNum - '0')
      }
      value
    }
    return values.sum()
  }

  override fun partA(): Any {
    return solve(2)
  }

  override fun partB(): Any {
    return solve(12)
  }

  companion object : Test(2025, 3, { Year2025Day3(it) })
}
