package org.vlegchilkin.aoc.year2020

import org.vlegchilkin.aoc.Solution
import org.vlegchilkin.aoc.Test

class Year2020Day10(input: String) : Solution {
  private val numbers = input.trim().split("\n").map { it.toInt() }
  private fun getJolts() = listOf(0) + numbers.sorted() + (numbers.max() + 3)
  override fun partA(): Int {
    val diffCount = getJolts().zipWithNext { a, b -> b - a }.groupingBy { it }.eachCount()
    return (diffCount[1] ?: 0) * (diffCount[3] ?: 0)
  }

  override fun partB(): Long {
    val jolts = getJolts()
    val dp = jolts.indices.map { 0L }.toLongArray()
    dp[0] = 1
    for (i in 1..<jolts.size) {
      for (j in i - 1 downTo 0) {
        if (jolts[i] - jolts[j] > 3) break
        dp[i] += dp[j]
      }
    }
    return dp.last()
  }

  companion object : Test(2020, 10, { Year2020Day10(it) })
}