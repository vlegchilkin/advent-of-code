package org.vlegchilkin.aoc.year2020

import org.vlegchilkin.aoc.Test
import org.vlegchilkin.aoc.Solution
import org.vlegchilkin.aoc.combinations
import org.vlegchilkin.aoc.trimSplitMap

class Year2020Day1(input: String) : Solution {
  private val numbers = input.trimSplitMap { it.toInt() }
  override fun partA(): Any {
    for ((a, b) in numbers.combinations(2)) {
      if (a + b == 2020) {
        return a * b
      }
    }
    return Unit
  }

  override fun partB(): Any {
    for ((a, b, c) in numbers.combinations(3)) {
      if (a + b + c == 2020) {
        return a * b * c
      }
    }
    return Unit
  }

  companion object : Test(2020, 1, { Year2020Day1(it) })
}